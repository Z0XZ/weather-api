def correct_voltage_for_temperature(voltage: float, temperature: float) -> float:
    """
    Justerer batterispenningen til å tilsvare romtemperatur (~25°C).
    """
    reference_temp = 22.7 # Temperatur under kalibrering
    mv_per_deg = 0.00125  # 1.25 mV pr °C
    delta_temp = reference_temp - temperature
    return voltage + (delta_temp * mv_per_deg)


def voltage_to_percent(voltage: float) -> int:
    """
    Konverterer (temperaturkompensert) LiPo-spenning til batteriprosent.
    """
    if voltage >= 4.20:
        return 100
    elif voltage >= 4.15:
        return 95
    elif voltage >= 4.11:
        return 90
    elif voltage >= 4.08:
        return 85
    elif voltage >= 4.02:
        return 80
    elif voltage >= 3.98:
        return 75
    elif voltage >= 3.95:
        return 70
    elif voltage >= 3.91:
        return 65
    elif voltage >= 3.87:
        return 60
    elif voltage >= 3.85:
        return 55
    elif voltage >= 3.84:
        return 50
    elif voltage >= 3.82:
        return 45
    elif voltage >= 3.8:
        return 40
    elif voltage >= 3.79:
        return 35
    elif voltage >= 3.77:
        return 30
    elif voltage >= 3.75:
        return 25
    elif voltage >= 3.73:
        return 20
    elif voltage >= 3.71:
        return 15
    elif voltage >= 3.69:
        return 10
    elif voltage >= 3.61:
        return 5
    else:
        return 0