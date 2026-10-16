
from cyclic_code import encode, decode

passed = 0
failed = 0

# Test all 16 possible 4-bit messages
for message in range(16):
    codeword = encode(message)

    # Test no error and every possible single-bit error
    for position in range(8):
        received = codeword

        if position != 0:
            received ^= 1 << (position - 1)

        result = decode(received)

        if result["corrected"] == codeword:
            passed += 1
        else:
            failed += 1
            print(
                f"FAIL: message={message:04b}, "
                f"position={position}, "
                f"received={received:07b}"
            )

print("\n===== TEST RESULTS =====")
print("Passed:", passed)
print("Failed:", failed)
print("Total:", passed + failed)

if failed == 0:
    print("ALL TESTS PASSED!")
else:
    print("SOME TESTS FAILED.")
