
GENERATOR = 0b1011


def remainder(poly):
    """Calculate polynomial division remainder over GF(2)."""
    while poly.bit_length() >= GENERATOR.bit_length():
        shift = poly.bit_length() - GENERATOR.bit_length()
        poly ^= GENERATOR << shift
    return poly


def encode(message):
    """Encode a 4-bit message into a systematic 7-bit codeword."""
    if not 0 <= message <= 15:
        raise ValueError("Message must be a 4-bit integer")

    shifted = message << 3
    return shifted | remainder(shifted)


def decode(received):
    """Correct a single-bit error using the syndrome lookup table."""
    if not 0 <= received <= 127:
        raise ValueError("Received word must be 7 bits")

    syndrome = remainder(received)
    corrected = received

    # Locate the single-bit error by its syndrome.
    error_position = None

    for position in range(7):
        error_pattern = 1 << position
        if remainder(error_pattern) == syndrome and syndrome != 0:
            error_position = position + 1
            corrected ^= error_pattern
            break

    if syndrome == 0:
        status = "No error detected"
    elif error_position is not None:
        status = f"Corrected bit {error_position} from the right"
    else:
        status = "Error not corrected"

    return {
        "syndrome": syndrome,
        "corrected": corrected,
        "message": corrected >> 3,
        "status": status,
    }
