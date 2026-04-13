from dataclasses import dataclass

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, StartInventoryPool

class KnowledgeDifficulty(Choice):
    """
    How much understanding of the games mechanics is expected to figure out the solution to a given medal/gift/etc.
    Casual: Expects the bare minimum, only tricks that are taught with in-game tutorials to beat the vanilla game.
    Standard: Incorporates hidden but usually intended or otherwise easy to intuit tech/ideas.
    Expert: Further includes some more advanced tech that is often only relevant to speedrunners.
    Master: Encompasses everything else from level-specific tech to extremely niche game quirks or nuances.
    """
    display_name = "Knowledge Difficulty"
    option_casual = 1
    option_standard = 2
    option_expert = 3
    option_master = 4
    default = 2

class ExecutionDifficulty(Choice):
    """
    How hard it is to actually execute a given solution to a given medal/gift/etc, assuming all knowledge.
    Casual: Can be done by a brand-new player with minimal hassle.
    Standard: Consistently doable by a player who has all aces, especially players with dev medals.
    Expert: Doable by a player who has all dev medals and is competent with advanced tech.
    Master: Unreasonably difficult solutions that are inconsistent/overly precise to the vast majority of players.
    """
    display_name = "Knowledge Difficulty"
    option_casual = 1
    option_standard = 2
    option_expert = 3
    option_master = 4
    default = 2

class MissionUnlockMethod(Choice):
    """
    How missions are unlocked to progress through the game.
    Ranks: Fills the pool with Neon Ranks, each mission requiring a number of ranks to unlock. See Rank Requirement.
    Missions: 1 Mission Unlock item is added to the pool per mission, each obtained unlocking the next locked mission.
    """
    display_name = "Mission Unlock Method"
    option_ranks = 1
    option_missions = 2
    default = 1

class MedalCap(Choice):
    """
    The highest medal to count for checks.
    Higher settings will result in more checks if Progressive Checks is enabled.
    """
    display_name = "Medal Cap"
    option_bronze = 1
    option_silver = 2
    option_gold = 3
    option_ace = 4
    option_dev = 5
    default = 4

class RankRequirement(Range):
    """
    The percentage of ranks required for the final mission out of the total amount of remaining checks in the pool.
    The rest of the mission requirements will scale accordingly.
    Only applies when Mission Unlock Method is set to Ranks.
    """
    display_name = "Rank Requirement"
    range_start = 1
    default = 30
    range_end = 100


class MissionCount(Range):
    """
    The amount of Missions for the game to have when mission randomization is enabled.
    Spreads evenly across all levels, then spreads across the later half with the remainder.
    """
    display_name = "Mission Count"
    range_start = 3
    default = 11
    range_end = 60

class ProgressiveChecks(DefaultOnToggle):
    """
    If every medal up to the medal cap should count for checks, or if only 1 check occurs for achieving the cap medal.
    If off, the number of checks will not change with changes to the medal cap.
    """
    display_name = "Progressive Checks"

class Traps(DefaultOnToggle):
    """
    Whether negative effects on the Neon White world are added to the item pool.
    """
    display_name = "Traps"

class Goal(Choice):
    """
    What the goal to complete should be.
    3bosses - Beat The Clocktower, The Third Temple, and Absolution with the goal medal cap.
    TrueEnding - Gather all memories and write Green into the Book of Life.
    """
    display_name = "Goal"
    option_3bosses = 1
    option_trueending = 2
    default = 1

class BossesCap(MedalCap):
    """
    The medal cap to use for the bosses if running the 3 bosses goal.
    """
    display_name = "3 Bosses Medal Cap"

class NeonWhiteDeathLink(DeathLink):
    __doc__ = (DeathLink.__doc__ + "\n\n    You can disable this or set it to give yourself a trap effect when " +  # pyright: ignore[reportOptionalOperand]
               "another player dies in the in-game mod options.")


@dataclass
class NeonWhiteOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: NeonWhiteDeathLink
    bad_effects: Traps
    progressive_checks: ProgressiveChecks
    medal_cap: MedalCap
    rank_requirement: RankRequirement
    mission_count: MissionCount
    difficulty_knowledge: KnowledgeDifficulty
    difficulty_execution: ExecutionDifficulty
    goal: Goal
    bosses_goal_cap: BossesCap
    unlock_method: MissionUnlockMethod
