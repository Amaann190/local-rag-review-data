"""Code where the generator of each RAG study with a local generator actually ran (audit variable `execution_host`).

Added after the third independent review: the `generator_location=local` rule counted hosted runtimes
(Kaggle, RunPod, shared research clouds) and studies that never state where inference ran as "local".
Coded from the extraction row (hardware, local_execution, notes) and, for local_unspecified, an explicit
statement in the saved abstract (records_dedup.json); the evidence column quotes it. See audit_codebook.md.
Writes audit/execution_host.csv.
"""
import csv, pathlib

H = pathlib.Path(__file__).parent
DEVICE, SERVER, CLAIMED, HOSTED, UNSTATED = "device", "server", "local_unspecified", "hosted", "not_stated"
CODES = {
    "R0015": (CLAIMED, "abstract: Llama3 model running locally through Ollama"),
    "R0029": (UNSTATED, "notes: local execution not stated"),
    "R0048": (UNSTATED, "notes: local execution not stated"),
    "R0069": (CLAIMED, "abstract: lightweight local language model (Qwen3-4B)"),
    "R0134": (DEVICE, "single consumer-grade GPU"),
    "R0269": (SERVER, "institutional hardware"),
    "R0287": (HOSTED, "Kaggle P100"),
    "R0326": (HOSTED, "H100 on Jetstream2 research cloud"),
    "R0336": (DEVICE, "Apple M1 laptop; x86 desktop without GPU"),
    "R0339": (UNSTATED, "abstract: locally deployable model; where experiments ran not stated"),
    "R0365": (DEVICE, "MacBook Air M3"),
    "R0372": (SERVER, "single 24 GB GPU machine"),
    "R0396": (HOSTED, "Kaggle 2x T4"),
    "R0526": (HOSTED, "free-tier Kaggle T4"),
    "R0587": (SERVER, "on-premises H100"),
    "R0594": (DEVICE, "Core i5 8 GB edge system"),
    "R0617": (UNSTATED, "unnamed small LLM vs GPT; no host stated"),
    "R0629": (DEVICE, "i9 + RTX 2070 device machine"),
    "R0667": (HOSTED, "Kaggle T4"),
    "R0691": (DEVICE, "i5 laptop target"),
    "R0742": (DEVICE, "local-only deployment on several hardware platforms"),
    "R0749": (UNSTATED, "open-source vs commercial LLMs; no host stated"),
    "R0750": (DEVICE, "three machines incl. laptop without GPU"),
    "R0767": (CLAIMED, "abstract: locally deployed LLM"),
    "R0773": (CLAIMED, "abstract: edge devices keep local documents; raw data not exposed"),
    "R0790": (SERVER, "RTX A6000"),
    "R0799": (UNSTATED, "simulation in NetworkX, no real devices"),
    "R0869": (DEVICE, "MacBook Pro device side"),
    "R0895": (SERVER, "two H100"),
    "R0929": (CLAIMED, "abstract: small, locally deployed models"),
    "R0966": (CLAIMED, "abstract: on-premises system; served locally"),
    "R0970": (CLAIMED, "abstract: locally deployed RAG pipeline"),
    "R0988": (DEVICE, "Android smartphones"),
    "R1095": (DEVICE, "Jetson Orin Nano"),
    "R1242": (DEVICE, "i7 desktop, GTX 1070 Ti"),
    "R1315": (SERVER, "single A100"),
    "R1334": (DEVICE, "consumer-grade hardware"),
    "R1342": (UNSTATED, "notes: local execution not explicit"),
    "R1355": (SERVER, "CUDA GPU, model not reported"),
    "R1366": (SERVER, "2x RTX A6000"),
    "R1378": (CLAIMED, "abstract: locally hosted RAG system"),
    "R1384": (UNSTATED, "notes: local execution not stated"),
    "R1394": (CLAIMED, "abstract: locally hosted models through Ollama"),
    "R1407": (UNSTATED, "notes: local execution not stated"),
    "R1598": (SERVER, "server-side V100; no on-device runs"),
    "R1642": (DEVICE, "RTX 4050 laptop"),
    "R1667": (DEVICE, "PC-grade hardware"),
    "R1673": (DEVICE, "commodity Android device"),
    "R1714": (UNSTATED, "private-QA framing; no host stated"),
    "R1812": (SERVER, "CUDA GPU, model not reported"),
    "R1833": (DEVICE, "RTX 4060 Ti desktop"),
    "R1870": (SERVER, "single-GPU engine"),
    "R1895": (SERVER, "generation on A800 servers"),
    "R1898": (DEVICE, "MacBook Air M3"),
    "R1925": (DEVICE, "consumer-grade local computer"),
    "R2025": (DEVICE, "Samsung Galaxy S23 Ultra"),
    "R2264": (CLAIMED, "abstract: served by a small local model"),
    "R2269": (SERVER, "in-house enterprise GPUs"),
    "R2298": (DEVICE, "consumer-grade workstation"),
    "R2318": (DEVICE, "consumer laptops via Ollama"),
    "R2346": (CLAIMED, "abstract: locally deployable LLM; on-premise deployment"),
    "R2360": (CLAIMED, "abstract: locally-deployed LLMs compared with API models"),
    "R2377": (UNSTATED, "notes: execution environment not stated"),
    "R2441": (HOSTED, "Grid'5000 shared research testbed"),
    "R2521": (CLAIMED, "abstract: four local LLMs, locally deployed assistants"),
    "R2559": (DEVICE, "Raspberry Pi 5; RTX 4090 desktop; MacBook Air M2"),
    "R2567": (UNSTATED, "notes: local execution implied by 4-bit quantization only"),
    "R2595": (DEVICE, "consumer-grade hardware under 4 GB"),
    "R2695": (UNSTATED, "notes: local execution on user hardware not verified"),
    "R2748": (HOSTED, "RAG backend on RunPod A5000 via ngrok"),
    "R2760": (HOSTED, "Kaggle P100"),
    "R2825": (DEVICE, "Raspberry Pi 5"),
    "R2836": (CLAIMED, "notes: generator self-hosted on vLLM"),
}
with open(H / "execution_host.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["record_id", "execution_host", "evidence"])
    for k in sorted(CODES):
        w.writerow([k, *CODES[k]])
print(len(CODES), "coded")
