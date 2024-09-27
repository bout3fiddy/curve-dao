import datetime

import boa
import math
TIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"


def get_datestring(ts):
    dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
    return dt.strftime(TIME_FORMAT)


def update_stableswap(
    pool,
    ramp_time_weeks,
    new_A,
    new_fee_bps,
    new_offpeg_fee_multiplier,
    proposal_time_weeks,
):
    SECONDS_PER_WEEK = 7 * 24 * 60 * 60
    FEE_SCALE = 10**6  # bps to int
    OFFPEG_FEE_MULTIPLIER_SCALE = 10**10  # bps to int

    ramp_time_seconds = int(ramp_time_weeks * SECONDS_PER_WEEK)
    proposal_time_seconds = int(proposal_time_weeks * SECONDS_PER_WEEK)
    scaled_fee = int(new_fee_bps * FEE_SCALE)
    scaled_offpeg_fee_multiplier = int(
        new_offpeg_fee_multiplier * OFFPEG_FEE_MULTIPLIER_SCALE
    )

    current_time = boa.env.evm.patch.timestamp
    future_A_time = current_time + ramp_time_seconds + proposal_time_seconds

    pool_address = pool.address.strip()
    actions = [
        (pool_address, "ramp_A", new_A, future_A_time),
        (pool_address, "set_new_fee", scaled_fee, scaled_offpeg_fee_multiplier),
    ]

    current_A = pool.A()
    current_fee_bps = pool.fee() / FEE_SCALE
    current_offpeg_multiplier = (
        pool.offpeg_fee_multiplier() / OFFPEG_FEE_MULTIPLIER_SCALE
    )
    ramp_start_time = future_A_time - ramp_time_seconds
    ramp_start_datestring = get_datestring(ramp_start_time)
    ramp_end_datestring = get_datestring(future_A_time)

    description = (
        f"Update StableswapNG parameters for pool {pool_address} with: "
        f"fee from {current_fee_bps} -> {new_fee_bps} bps, "
        f"offpeg multiplier from {current_offpeg_multiplier} -> {new_offpeg_fee_multiplier}, "
        f"amplification factor from {current_A} -> {new_A} ramped over {ramp_time_weeks} weeks "
        f"starting on {ramp_start_datestring} and ending on {ramp_end_datestring}."
    )

    return actions, description


def update_twocrypto_ng(
        pool,
        ramp_time_weeks,
        new_A,
        new_gamma,
        new_mid_fee,
        new_out_fee,
        new_fee_gamma,
        new_allowed_extra_profit,
        new_adjustment_step,
        new_ma_time,
        proposal_time_weeks,
):
    SECONDS_PER_WEEK = 7 * 24 * 60 * 60

    ramp_time_seconds = int(ramp_time_weeks * SECONDS_PER_WEEK)
    proposal_time_seconds = int(proposal_time_weeks * SECONDS_PER_WEEK)

    current_time = boa.env.evm.patch.timestamp
    future_A_time = current_time + ramp_time_seconds + proposal_time_seconds

    pool_address = pool.address.strip()
    actions = [
        (pool_address, "ramp_A_gamma", new_A, new_gamma, future_A_time),    # adjust A and gamma
        (pool_address, "apply_new_parameters", new_mid_fee, new_out_fee, new_fee_gamma, new_allowed_extra_profit, new_adjustment_step, int(new_ma_time / math.log(2)))
    ]

    current_A = pool.A()
    current_gamma = pool.gamma()
    current_mid_fee = pool.mid_fee()
    current_out_fee = pool.out_fee()
    current_fee_gamma = pool.fee_gamma()
    current_allowed_extra_profit = pool.allowed_extra_profit()
    current_adjustment_step = pool.adjustment_step()
    current_ma_time = pool.ma_time()

    ramp_start_time = future_A_time - ramp_time_seconds
    ramp_start_datestring = get_datestring(ramp_start_time)
    ramp_end_datestring = get_datestring(future_A_time)

    description = (
        f"Update TwocryptoNG parameters for pool {pool_address} with: "
        f"mid_fee from {current_mid_fee} -> {new_mid_fee}, "
        f"out_fee from {current_out_fee} -> {new_out_fee}, "
        f"fee_gamma from {current_fee_gamma} -> {new_fee_gamma}, "
        f"allowed_extra_profit from {current_allowed_extra_profit} -> {new_allowed_extra_profit}, "
        f"adjustment_step from {current_adjustment_step} -> {new_adjustment_step}, "
        f"ma_time from {current_ma_time} -> {new_ma_time}, "
        f"amplification factor from {current_A} -> {new_A} ramped over {ramp_time_weeks} weeks "
        f"gamma from {current_gamma} -> {new_gamma} ramped over {ramp_time_weeks} weeks "
        f"starting on {ramp_start_datestring} and ending on {ramp_end_datestring}."
    )

    return actions, description


def update_twocrypto(
    pool,
    ramp_time_weeks,
    new_A,
    new_gamma,
    new_mid_fee,
    new_out_fee,
    new_admin_fee,
    new_fee_gamma,
    new_allowed_extra_profit,
    new_adjustment_step,
    new_ma_half_time,
    proposal_time_weeks,
):
    SECONDS_PER_WEEK = 7 * 24 * 60 * 60
    CRYPTOSWAP_OWNER_PROXY = "0x5a8fdC979ba9b6179916404414F7BA4D8B77C8A1"


    ramp_time_seconds = int(ramp_time_weeks * SECONDS_PER_WEEK)
    proposal_time_seconds = int(proposal_time_weeks * SECONDS_PER_WEEK)

    current_time = boa.env.evm.patch.timestamp
    future_A_time = current_time + ramp_time_seconds + proposal_time_seconds

    pool_address = pool.address.strip()
    actions = [
        (CRYPTOSWAP_OWNER_PROXY, "ramp_A_gamma", pool, new_A, new_gamma, future_A_time),
        (CRYPTOSWAP_OWNER_PROXY, "commit_new_parameters", pool, new_mid_fee, new_out_fee, new_admin_fee, new_fee_gamma, new_allowed_extra_profit, new_adjustment_step, new_ma_half_time)
    ]

    current_A = pool.A()
    current_gamma = pool.gamma()
    current_mid_fee = pool.mid_fee()
    current_out_fee = pool.out_fee()
    current_admin_fee = pool.admin_fee()
    current_fee_gamma = pool.fee_gamma()
    current_allowed_extra_profit = pool.allowed_extra_profit()
    current_adjustment_step = pool.adjustment_step()
    current_ma_half_time = pool.ma_half_time()

    ramp_start_time = future_A_time - ramp_time_seconds
    ramp_start_datestring = get_datestring(ramp_start_time)
    ramp_end_datestring = get_datestring(future_A_time)

    description = (
        f"Update Twocrypto parameters for pool {pool_address} with: "
        f"mid_fee from {current_mid_fee} -> {new_mid_fee}, "
        f"out_fee from {current_out_fee} -> {new_out_fee}, "
        f"admin_fee from {current_admin_fee} -> {new_admin_fee}, "
        f"fee_gamma from {current_fee_gamma} -> {new_fee_gamma}, "
        f"allowed_extra_profit from {current_allowed_extra_profit} -> {new_allowed_extra_profit}, "
        f"adjustment_step from {current_adjustment_step} -> {new_adjustment_step}, "
        f"ma_half_time from {current_ma_half_time} -> {new_ma_half_time}, "
        f"amplification factor from {current_A} -> {new_A} and "
        f"gamma from {current_gamma} -> {new_gamma} ramped over {ramp_time_weeks} weeks "
        f"starting on {ramp_start_datestring} and ending on {ramp_end_datestring}."
    )

    return actions, description
