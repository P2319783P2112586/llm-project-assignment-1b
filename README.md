<<<<<<< HEAD
# llm-project-assignment1b
AI Large Language Model - Assignment 1B
=======
# AI (Large Language Model) — Assignment 1B

## Project Overview

This project implements and evaluates Google's `google/gemma-2b-it` instruction-tuned language model. It demonstrates a local setup for loading a pre-trained open-weight LLM, generating conversational responses, applying 4-bit quantization, and evaluating selected model capabilities and limitations.

The recorded implementation was tested on an Apple Silicon macOS environment using the PyTorch MPS backend.

## Features

- Load the `google/gemma-2b-it` model and its tokenizer from Hugging Face.
- Detect the available compute device (Apple MPS, NVIDIA CUDA, or CPU).
- Configure 4-bit quantization with BitsAndBytes.
- Generate responses using the model's chat template.
- Run an interactive terminal chat application.
- Run automated tests for factual response matching, code-generation response structure, and input validation.
- Document qualitative evaluation in `RESULTS.md`.

## Project Structure

```text
llm-project-assignment1b/
├── src/
│   ├── __init__.py
│   └── model.py
├── tests/
│   └── test_model.py
├── video/
│   ├── 1-Installation/
│   ├── 2-Implementation/
│   └── 3-Testing/
├── demo.py
├── requirements.txt
├── README.md
├── RESULTS.md
└── .gitignore
```

## Tested Environment

The following versions were recorded in the working environment:

| Component | Version / configuration |
|---|---|
| Python | 3.14.8 |
| PyTorch | 2.15.0 |
| Transformers | 5.22.1 |
| Accelerate | 1.15.0 |
| BitsAndBytes | 0.50.2 |
| Hugging Face Hub | 2.4.0 |
| kernels | 0.18.0 |
| Compute device | Apple MPS |
| Model | `google/gemma-2b-it` |
| Quantization | 4-bit; the model reported `Quantized: True` |

`requirements.txt` records the installed package versions using `pip freeze`. It reflects the tested environment and may be platform-specific.

## Prerequisites

- Python 3.10 or later (the recorded environment used Python 3.14.8).
- Git.
- A Hugging Face account.
- Access to the `google/gemma-2b-it` model repository. Review and accept the model's applicable Google Gemma terms on its Hugging Face model page before downloading it.
- Sufficient memory and disk space for model files and inference. The first model download in the recorded run downloaded approximately 4.37 GB of weight files.

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/P2319783P2112586/llm-project-assignment1b.git
cd llm-project-assignment1b
```

Create and activate a virtual environment on macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Upgrade pip and install the pinned dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Check for dependency conflicts:

```bash
python -m pip check
```

### Hugging Face Authentication

After accepting the model terms on the model page, authenticate with Hugging Face:

```bash
hf auth login
hf auth whoami
```

The login command supports browser-based authentication or an access token. Never put a Hugging Face token in source code, `requirements.txt`, `README.md`, a video, or a public GitHub commit.

To verify access to the model configuration file:

```bash
hf download google/gemma-2b-it config.json
```

## Run the Interactive Demo

From the repository root, with the virtual environment active:

```bash
python demo.py
```

Enter a prompt when the `You:` prompt appears. Enter `quit` or `exit` to close the application.

The first run downloads the model files from Hugging Face. Later runs can use the local Hugging Face cache. The implementation selects an available device and configures 4-bit quantization by default.

## Run the Tests

Run the test suite from the repository root:

```bash
python -m unittest discover tests
```

The current test module contains two model-based integration tests and two input-validation tests. The integration tests load the Gemma model and therefore require model access, sufficient resources, and a working inference backend.

The recorded run completed with:

```text
Ran 4 tests in 13.012s

OK
```

This result applies to the recorded test run; it does not establish that the model is always factually correct or that generated code is executable.

## Experimental Results

See [`RESULTS.md`](RESULTS.md) for the experimental environment, observed model responses, reasoning failure case, automated test summary, and overall evaluation.

Before final submission, make sure the report includes the actual observed response for the assignment's haiku prompt and the actual observed response for the safety prompt. Do not claim a safety refusal or describe a response as a haiku unless the recorded output supports that conclusion.

## Screen-Recording Videos

Add the three required MP4 recordings to the corresponding folders below, and replace the placeholder links with the final filenames. Use the exact naming convention specified in the assignment brief, including the correct student number(s) and project title.

1. **Installation** — repository clone, virtual environment, dependency installation, and Hugging Face authentication.  
   `video/1-Installation/` — [Add the final installation video link]
2. **Implementation and Demo** — explain `src/model.py`, run `demo.py`, and demonstrate at least three different prompts.  
   `video/2-Implementation/` — [Add the final implementation video link]
3. **Testing and Results** — run the unit tests, show `RESULTS.md`, and demonstrate all five qualitative-analysis prompts with the model.  
   `video/3-Testing/` — [Add the final testing video link]

## Security and Reproducibility Notes

- Do not commit access tokens, passwords, private keys, or local environment files.
- The virtual environment (`venv/`) and Python cache files should not be committed.
- Model weights are downloaded from Hugging Face and are not stored in this Git repository.
- The package versions in `requirements.txt` were captured from the tested machine. Reproduction on a different operating system or hardware may require environment-specific changes.

## Model Reference

- Hugging Face model: <https://huggingface.co/google/gemma-2b-it>
- Hugging Face CLI documentation: <https://huggingface.co/docs/huggingface_hub/guides/cli>
>>>>>>> 1621181 (Complete Gemma 2B Assignment 1B implementation)
