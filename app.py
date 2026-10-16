
import streamlit as st
import pandas as pd

GENERATOR = 0b1011


def remainder(poly):
    while poly.bit_length() >= GENERATOR.bit_length():
        shift = poly.bit_length() - GENERATOR.bit_length()
        poly ^= GENERATOR << shift
    return poly


def encode(message):
    shifted = message << 3
    return shifted | remainder(shifted)


def syndrome_table():
    rows = []
    for position in range(1, 8):
        value = remainder(1 << (position - 1))
        rows.append({
            "Bit position (from right)": position,
            "Error pattern": format(1 << (position - 1), "07b"),
            "Syndrome": format(value, "03b")
        })
    return rows


def decode(received):
    syndrome = remainder(received)

    if syndrome == 0:
        return received, "No error detected", syndrome

    for position in range(7):
        if remainder(1 << position) == syndrome:
            corrected = received ^ (1 << position)
            return (
                corrected,
                f"Corrected bit {position + 1} from the right",
                syndrome
            )

    return None, "Error could not be located", syndrome


st.set_page_config(
    page_title="Cyclic Code Lab",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Cyclic Code Encoder & Decoder")
st.caption("Hamming (7, 4) | Generator polynomial: g(x) = x³ + x + 1")

st.divider()

# 1. Encoder
st.header("1. Message Encoder")

message_text = st.text_input(
    "Enter a 4-bit binary message",
    value="1011",
    max_chars=4
)

if len(message_text) != 4 or any(b not in "01" for b in message_text):
    st.warning("Enter exactly four binary digits, for example 1011.")
    st.stop()

message = int(message_text, 2)
codeword = encode(message)

col1, col2 = st.columns(2)
col1.metric("Original message", message_text)
col2.metric("Encoded codeword", format(codeword, "07b"))

st.divider()

# 2. Error simulation
st.header("2. Transmission Error Simulator")
st.write("Select bit positions to flip. Position 1 is the rightmost bit.")

positions = st.multiselect(
    "Select error positions",
    options=list(range(1, 8)),
    default=[1]
)

received = codeword
for position in positions:
    received ^= 1 << (position - 1)

col1, col2, col3 = st.columns(3)
col1.metric("Transmitted", format(codeword, "07b"))
col2.metric("Received", format(received, "07b"))
col3.metric("Number of flipped bits", len(positions))

# 3. Bit-by-bit visualizer
st.subheader("Bit-by-bit comparison")

bit_rows = []
for position in range(7, 0, -1):
    bit_index = position - 1
    sent_bit = (codeword >> bit_index) & 1
    received_bit = (received >> bit_index) & 1

    bit_rows.append({
        "Bit position": position,
        "Transmitted bit": sent_bit,
        "Received bit": received_bit,
        "Changed?": "YES" if sent_bit != received_bit else "No"
    })

st.dataframe(
    pd.DataFrame(bit_rows),
    hide_index=True,
    use_container_width=True
)

st.divider()

# 4. Syndrome decoder
st.header("3. Syndrome Decoder")

corrected, status, syndrome = decode(received)

col1, col2 = st.columns(2)
col1.metric("Calculated syndrome", format(syndrome, "03b"))
col2.write("**Decoder status**")
col2.write(status)

if corrected is not None:
    st.write("**Corrected codeword:**", format(corrected, "07b"))
    st.write("**Decoded message:**", format(corrected >> 3, "04b"))

    corrected_rows = []
    for position in range(7, 0, -1):
        bit_index = position - 1
        sent_bit = (codeword >> bit_index) & 1
        received_bit = (received >> bit_index) & 1
        corrected_bit = (corrected >> bit_index) & 1

        corrected_rows.append({
            "Position": position,
            "Sent": sent_bit,
            "Received": received_bit,
            "Corrected": corrected_bit,
            "Matches original?": (
                "Yes" if corrected_bit == sent_bit else "No"
            )
        })

    st.subheader("Correction verification")
    st.dataframe(
        pd.DataFrame(corrected_rows),
        hide_index=True,
        use_container_width=True
    )

    if corrected == codeword:
        st.success("Original codeword recovered successfully.")
    else:
        st.warning(
            "Output differs from the transmitted codeword. "
            "Multiple-bit errors can cause miscorrection."
        )

# 5. Lookup table
st.divider()
st.header("4. Syndrome Lookup Table")
st.write("Each row shows the syndrome produced by a single-bit error.")

st.dataframe(
    pd.DataFrame(syndrome_table()),
    hide_index=True,
    use_container_width=True
)

st.info(
    "This Hamming (7, 4) decoder corrects single-bit errors. "
    "It cannot reliably correct arbitrary multiple-bit errors."
)
