fuel_amount:
- unidade: definida em consumption_profiles
- domínio: > 0
- origem: amostrado + ajustado por empresa + eficiência

fuel_amount_final = (base_consumption × company_multiplier) / efficiency_factor
energy_kwh = fuel_amount × energy_factor

co2_emission:
IF fuel_type ≠ electric:
    = fuel_amount × co2_factor

IF fuel_type = electric:
    = energy_kwh × emission_factor

co2_final = co2_base × (1 + ε)

ε ~ Normal(0, noise_std)
Domínio: ε ∈ (-1, +∞)
Restrição: co2_final ≥ 0