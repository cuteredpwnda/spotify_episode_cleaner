import os
import click

from helper import ep_filter, data_handler


@click.command()
@click.option(
    "-p",
    "--played",
    type=bool,
    default=True,
    help="Remove played episodes, set to False to keep played episodes",
)
@click.option(
    "-ap",
    "--almost_played",
    type=bool,
    default=True,
    help="Remove almost played episodes, set to False to keep almost played episodes",
)
@click.option(
    "-app",
    "--almost_played_percent",
    type=int,
    default=95,
    help="Define the percentage of the episode that is considered played",
)
@click.option(
    "-ot",
    "--older_than",
    type=int,
    default=365,
    help="Remove episodes older than x days, default is 365",
)
@click.option("-rs", "--remove_show", type=str, help="Remove episodes from show x")
@click.option("-ks", "--keep_show", type=str, help="Keep episodes from show x, can either be the name, the spotify id or the uri")
@click.option("-sc", "--skip_cache", type=bool, default=False, is_flag=True, help="Skip reading from cache")
def main(
    played: bool,
    almost_played: bool,
    almost_played_percent: int,
    older_than: int,
    remove_show: str,
    keep_show: str,
    skip_cache: bool,
):
    df = data_handler.get_your_saved_episodes(skip_cache = skip_cache)
    total_eps = df.shape[0]
    to_del = ep_filter.your_episodes(
        df, played, almost_played, almost_played_percent, older_than, remove_show
    )    
    print(f"keeping {total_eps - to_del.shape[0]} of {total_eps} episodes based on your filters")
    if keep_show:
        to_del = ep_filter.keep_show(to_del, keep_show)

    if to_del.empty:
        print("no episodes to delete based on your filters")
        exit(0)
    
    print(f"deleting {to_del.shape[0]} of {total_eps} episodes...")
    # delete episodes
    data_handler.delete_from_your_episodes(to_del)

    # clear cache, to get fresh data next time
    os.remove(data_handler.CACHE_FILE)    
    exit(0)

if __name__ == "__main__":
    main()
