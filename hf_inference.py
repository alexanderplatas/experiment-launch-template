import json
import os
import time

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

"""
# -------------------------------------------------------------------------------------------------------- #

Este script realiza inferencia sobre el LLM seleccionado de HuggingFace mediante pipelines de transformers

Parámetros:
- model_id: Nombre del modelo a usar (huggingface id)
- cuda_device: Número de GPUs a usar (Ej. "0", "0,1,2")
- max_tokens: Máximo de tokens a generar por el modelo
- max_attempts_per_request: Número de veces a reintentar en caso de error
- cache_dir: Directorio donde se almacena el modelo. IMPORTANTE: Controlar el espacio (borrar al terminar)
- temperature: Temperatura del modelo (aleatoriedad de generación)

# -------------------------------------------------------------------------------------------------------- #
"""

def get_response():
    attempt = 1
    response_text = ""

    # --------------- Apply chat template  ---------------- #

    messages = [{
        "role": "user",
        "content": f"{prompt}",
    }]

    # -------------------- Inference ---------------------- #

    while attempt <= parameters["max_attempts_per_request"]:

        try:  # Try "max_attempts_per_request" times

            response_raw = generator(
                messages,
                max_new_tokens=parameters['max_tokens'],
                do_sample=False,
                temperature=parameters['temperature']
            )

            response_text = response_raw[0]["generated_text"][-1]['content']
            break

        except Exception as e:

            print(f"Request failed> [Attempt {attempt}/{parameters['max_attempts_per_request']}] {e}")
            attempt += 1

    # ------------------ Return response ------------------ #

    return response_text


if __name__ == '__main__':

    # ------------------ Load parameters ------------------ #

    # En este json se seleccionan los parámetros de ejecución (modelo,
    with open('configs/hf_inference.json', 'r') as p:
        parameters = json.load(p)

    os.environ["CUDA_VISIBLE_DEVICES"] = parameters["cuda_device"]

    print("\n" + " Parameters ".center(80, '='))
    for k, v in parameters.items():
        print(f" {k}: {v}")
    print("".center(80, '=') + '\n')

    prompt = """Hello, LLM!"""  # <--- Here your prompt (or load from file)

    # ------------- Load model and tokenizer -------------- #

    tokenizer = AutoTokenizer.from_pretrained(parameters['model_id'], cache_dir=parameters['cache_dir'], trust_remote_code=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    model = AutoModelForCausalLM.from_pretrained(
        parameters['model_id'],
        cache_dir=parameters['cache_dir'],
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

    # ---------------- Get model response ----------------- #

    start_time = time.time()
    response = get_response()
    end_time = time.time()

    # ------------------- Print result -------------------- #

    print("\n" + f" Prompt ".center(80, '-'))
    print(prompt)

    print("\n" + f" Response ".center(80, '-'))
    print(response)  # Recommended: Save response

    print("\n" + f"".center(80, '-'))
    print(f"Time> {round(end_time - start_time, 2)}s")

    print("\n" + f"".center(80, '='))
    print(" Finished ".center(80, ' ') + "\n")
