import numpy as np
import os
import pandas as pd
import re

def clean_data(file_path: str, directory: str = ''):
    '''
    clean_data(file_path: str, directory: str = '')

    Clean the data frame to fix column names and types

    Parameters
    ----------
    file_path: str
        Path to the raw dataframe scraped from Pro Football Reference
    directory: str, optional
        Directory to write output CSV files

    Returns
    -------
    ff_year: DataFrame
        Dataframe with cleaned column names and coerced types

    Notes
    -----
    Also outputs processed CSV files into specified directory
    '''
    ff_year = pd.read_csv(file_path)
    def fix_feature_name(prefix: str, name: str) -> str:
        '''
        fix_feature_name(prefix: str, name: str)

        Adjust column names to be more descriptive (collapse prefix and name into one)

        Parameters
        ----------
        prefix: str
            The first part of the column name, with periods and 'Unnamed'

        name: str
            The second part of the column name

        Returns
        -------
        str
            String of the fixed column name, with prefix and name separated by '-'
        '''
        tmp_prefix = re.split('\\.', prefix)[0]
        fixed_prefix = [tmp_prefix.lower() + '_' if re.search('Unnamed', tmp_prefix) is None else ''][0]
        return fixed_prefix + name.lower()
    col_names = ff_year.iloc[0, :].reset_index()
    col_names.columns = ['prefix', 'name']
    fixed_names = [fix_feature_name(col_prefix, col_name) for col_prefix, col_name in zip(col_names.prefix, col_names.name)]
    
    # Keep original column names
    original_names = ff_year.iloc[0, :].reset_index(drop = True)
    # Adjust column names, remove extraneous rows
    ff_year.columns = fixed_names
    ff_year = ff_year[ff_year.rk != original_names[0]].reset_index(drop = True)
    # Remove extraneous information from the player column
    ff_year.player = [re.split('[+*^]+$', player)[0] for player in ff_year.player]

    # Coerce numeric columns to float, int
    numeric_columns = ff_year.drop(columns = ['player', 'tm', 'fantpos']).columns
    for col in numeric_columns:
        ff_year[col] = pd.to_numeric(ff_year[col])
    # Coerce categorical columns to factors
    factor_columns = ['tm', 'fantpos']
    for col in factor_columns:
        ff_year[col] = ff_year[col].astype('category')

    # Drop criteria (meet one of the following):
    # Position not in [QB, RB, WR, TE]
    # Played 4 or fewer games
    ff_year = ff_year[ff_year.fantpos.isin(['QB', 'RB', 'WR', 'TE'])]
    ff_year = ff_year[ff_year.games_g > 4]

    # Position-specific criteria
    # QB: 100 PPR points
    ff_year = ff_year[(ff_year.fantasy_ppr >= 100) | (ff_year.fantpos != 'QB')]
    # All other positions: 50 PPR points
    ff_year = ff_year[(ff_year.fantasy_ppr >= 50) | (ff_year.fantpos == 'QB')]

    # NA values treated as 0
    ff_year.loc[:, 'games_g':'fantasy_vbd'] = ff_year.loc[:, 'games_g':'fantasy_vbd'].fillna(0)

    # Remove different fantasy football scoring systems
    ff_year.drop(columns = ['rk', 'fantasy_dkpt', 'fantasy_fdpt', 'fantasy_vbd', 'fantasy_posrank', 'fantasy_ovrank'], inplace = True)

    # Only use game-adjusted columns
    columns_to_adjust = [feature for feature in ff_year.columns
                         if (ff_year.dtypes[feature] in [float, int])
                         and (re.match('games', feature) is None)
                         and (re.match('age', feature) is None)]
    adjusted_columns = pd.DataFrame({stat + '_adj': ff_year[stat] / np.sqrt(ff_year.games_g / ff_year.games_g.max())
                                     for stat in columns_to_adjust})
    ff_year = pd.concat([ff_year, adjusted_columns], axis = 1)      

    file_stub = re.findall('(?<=\\/)[\w\-]+(?=\\.csv)', file_path)[0]
    ff_year['year'] = int(re.findall('\d+', file_stub)[0])
    return ff_year

ff_year_files = ['data/raw/' + file_name for file_name in sorted(os.listdir('data/raw/')) if re.search('\\.csv$', file_name) is not None]
ff_year_dfs = [clean_data(file_path = file, directory = 'data/processed/') for file in ff_year_files]

# Add response variable
for yr in range(len(ff_year_dfs) - 1):
    response = ff_year_dfs[yr + 1][['player', 'fantasy_ppr']].rename(columns = {'fantasy_ppr': 'NEXT_YR_PPR'}).set_index('player')
    ff_year_dfs[yr] = ff_year_dfs[yr].set_index('player').join(other = response, on = 'player', how = 'inner').reset_index()

# Save most recent year as test data
test_df = ff_year_dfs[-1]
test_df.to_csv('data/processed/test-data.csv', index = False)
# Save all other years as modeling data
modeling_df = pd.concat(ff_year_dfs[:-1]).reset_index(drop = True)
modeling_df.to_csv('data/processed/modeling-data.csv', index = False)

# Remove non-adjusted and extraneous columns
modeling_df.drop(columns = modeling_df.loc[:, 'passing_cmp':'fantasy_ppr'].columns.to_list() + \
    ['games_gs', 'rushing_y/a_adj', 'receiving_y/r_adj', 'fantasy_fantpt_adj', 'fantasy_ppr_adj'],
    inplace = True)
modeling_df.to_csv('data/processed/modeling-data-reduced.csv', index = False)