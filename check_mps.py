import time, torch

def bench(device):
    x = torch.randn(4096, 4096, device=device)
    torch.matmul(x, x)
    if device == "mps": torch.mps.synchronize()
    start = time.perf_counter()
    for _ in range(20):
        torch.matmul(x, x)
    if device == "mps": torch.mps.synchronize()
    return time.perf_counter() - start

print(f"CPU: {bench('cpu'):.2f} seconds")
print(f"GPU: {bench('mps'):.2f} seconds")
