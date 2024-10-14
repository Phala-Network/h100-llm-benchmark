
## Latency tests

- Input length: 32 tokens.
- Output length: 128 tokens.
- Batch size: fixed (8).
- Models: llama-3.1 8B, llama-3 70B, mixtral 8x7B.
- Evaluation metrics: end-to-end latency (mean, median, p99).


| Test name             | GPU   |   Mean latency (ms) |   Median latency (ms) |   P99 latency (ms) |
|:----------------------|:------|--------------------:|----------------------:|-------------------:|
| latency_gemma2-27b    | H200  |            2414.87  |              2414.51  |            2418.55 |
| latency_llama70B      | H200  |           28675.9   |             28676.4   |           28687.3  |
| latency_Phi3-14B-128k | H200  |            1625.26  |              1624.89  |            1628.15 |
| latency_llama8B       | H200  |             921.218 |               913.466 |            1006.8  |


## Throughput tests

- Input length: randomly sample 200 prompts from ShareGPT dataset (with fixed random seed).
- Output length: the corresponding output length of these 200 prompts.
- Batch size: dynamically determined by vllm to achieve maximum throughput.
- Models: llama-3.1 8B, llama-3 70B, mixtral 8x7B.
- Evaluation metrics: throughput.


| Test name                | GPU   |   Tput (req/s) |
|:-------------------------|:------|---------------:|
| throughput_llama70B      | H200  |        2.18718 |
| throughput_Phi3-14B-128k | H200  |       12.7573  |
| throughput_llama8B       | H200  |       29.4577  |
| throughput_gemma2-27b    | H200  |       11.9429  |


## Serving tests

- Input length: randomly sample 200 prompts from ShareGPT dataset (with fixed random seed).
- Output length: the corresponding output length of these 200 prompts.
- Batch size: dynamically determined by vllm and the arrival pattern of the requests.
- **Average QPS (query per second)**: 1, 4, 16 and inf. QPS = inf means all requests come at once. For other QPS values, the arrival time of each query is determined using a random Poisson process (with fixed random seed).
- Models: llama-3.1 8B, llama-3 70B, mixtral 8x7B.
- We also added a speculative decoding test for llama-3 70B, under QPS 2
- Evaluation metrics: throughput, TTFT (time to the first token, with mean, median and p99), ITL (inter-token latency, with mean, median and p99).


| Test name                                  | GPU   |   Tput (req/s) |   Mean TTFT (ms) |   Median TTFT (ms) |   P99 TTFT (ms) |   Mean ITL (ms) |   Median ITL (ms) |   P99 ITL (ms) |
|:-------------------------------------------|:------|---------------:|-----------------:|-------------------:|----------------:|----------------:|------------------:|---------------:|
| serving_Phi3-14B-128k_tp1_sharegpt_qps_4   | H200  |       3.83817  |          67.5655 |            64.6161 |        102.226  |        27.8034  |          23.709   |       103.727  |
| serving_llama8B_tp1_sharegpt_qps_4         | H200  |       3.91446  |          40.7345 |            33.9398 |        136.144  |        11.924   |          11.4048  |        27.1082 |
| serving_gemma27b_tp1_sharegpt_qps_16       | H200  |       7.0904   |       18316.8    |         14784.6    |      46388.4    |       142.72    |         147.847   |       474.561  |
| serving_llama70B_tp1_sharegpt_qps_1        | H200  |       0.893545 |         299.272  |           336.985  |        833.7    |       246.194   |         239.131   |       312.603  |
| serving_gemma27b_tp1_sharegpt_qps_4        | H200  |       3.78897  |         104.436  |            72.2619 |        248.423  |        36.8354  |          30.5109  |       137.354  |
| serving_llama70B_tp1_sharegpt_qps_4        | H200  |       2.39213  |        1196.68   |           540.716  |       7057.81   |       347.9     |         326.541   |       641.468  |
| serving_gemma27b_tp1_sharegpt_qps_1        | H200  |       0.991682 |          77.6896 |            56.7014 |        151.386  |        22.9326  |          21.7848  |        58.528  |
| serving_llama70B_tp1_sharegpt_qps_16       | H200  |       2.58313  |       44484.6    |         23836.1    |     157147      |       366.495   |         339.684   |       639.789  |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_16  | H200  |       6.82811  |       20066.8    |         12178.3    |      55927.8    |       136.223   |         150.407   |       293.171  |
| serving_llama70B_tp1_sharegpt_qps_inf      | H200  |       2.57113  |       67523.5    |         42070.9    |     221519      |       367.137   |         339.664   |       643.244  |
| serving_llama8B_tp1_sharegpt_qps_16        | H200  |       9.46838  |       15274.6    |         13725.1    |      33896.9    |       107.675   |         122.181   |       244.653  |
| serving_llama8B_tp1_sharegpt_qps_inf       | H200  |      10.525    |       37767.7    |         32781.6    |      82461.6    |       105.747   |         137.145   |       191.637  |
| serving_gemma27b_tp1_sharegpt_qps_inf      | H200  |       7.21072  |       48086      |         46735.8    |     106648      |       143.679   |         144.949   |       409.875  |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_1   | H200  |       0.993651 |          54.5558 |            51.9069 |        107.845  |        15.7842  |          14.8229  |        51.7429 |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_inf | H200  |       7.21274  |       45785.3    |         43124.6    |     111318      |       135.134   |         147.053   |       187.651  |
| serving_llama8B_tp1_sharegpt_qps_1         | H200  |       0.993912 |          38.3482 |            29.0162 |         94.7463 |         8.60381 |           8.30276 |        16.0659 |


## json version of the benchmarking tables

This section contains the data of the markdown tables above in JSON format. 
You can load the benchmarking tables into pandas dataframes as follows:

```python
import json
import pandas as pd

benchmarking_results_json = """The json string"""
benchmarking_results = json.loads(benchmarking_results_json)
latency_results = pd.DataFrame.from_dict(benchmarking_results["latency"])
throughput_results = pd.DataFrame.from_dict(benchmarking_results["throughput"])
serving_results = pd.DataFrame.from_dict(benchmarking_results["serving"])
```

The json string for all benchmarking tables:
```json
{"latency": {"Test name": {"0": "latency_gemma2-27b", "1": "latency_llama70B", "2": "latency_Phi3-14B-128k", "3": "latency_llama8B"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200"}, "Mean latency (ms)": {"0": 2414.8746706665406, "1": 28675.915970999755, "2": 1625.2587303999462, "3": 921.2177123331154}, "Median latency (ms)": {"0": 2414.5072150004125, "1": 28676.394058998994, "2": 1624.885462999373, "3": 913.4660290001193}, "P99 latency (ms)": {"0": 2418.550312218904, "1": 28687.30314671946, "2": 1628.1472031398516, "3": 1006.8028317395874}}, "throughput": {"Test name": {"0": "throughput_llama70B", "1": "throughput_Phi3-14B-128k", "2": "throughput_llama8B", "3": "throughput_gemma2-27b"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200"}, "Tput (req/s)": {"0": 2.1871831225359264, "1": 12.757253134994153, "2": 29.457698697610706, "3": 11.942856887441872}}, "serving": {"Test name": {"0": "serving_Phi3-14B-128k_tp1_sharegpt_qps_4", "1": "serving_llama8B_tp1_sharegpt_qps_4", "2": "serving_gemma27b_tp1_sharegpt_qps_16", "3": "serving_llama70B_tp1_sharegpt_qps_1", "4": "serving_gemma27b_tp1_sharegpt_qps_4", "5": "serving_llama70B_tp1_sharegpt_qps_4", "6": "serving_gemma27b_tp1_sharegpt_qps_1", "7": "serving_llama70B_tp1_sharegpt_qps_16", "8": "serving_Phi3-14B-128k_tp1_sharegpt_qps_16", "9": "serving_llama70B_tp1_sharegpt_qps_inf", "10": "serving_llama8B_tp1_sharegpt_qps_16", "11": "serving_llama8B_tp1_sharegpt_qps_inf", "12": "serving_gemma27b_tp1_sharegpt_qps_inf", "13": "serving_Phi3-14B-128k_tp1_sharegpt_qps_1", "14": "serving_Phi3-14B-128k_tp1_sharegpt_qps_inf", "15": "serving_llama8B_tp1_sharegpt_qps_1"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200", "4": "H200", "5": "H200", "6": "H200", "7": "H200", "8": "H200", "9": "H200", "10": "H200", "11": "H200", "12": "H200", "13": "H200", "14": "H200", "15": "H200"}, "Tput (req/s)": {"0": 3.838173332872599, "1": 3.914462589057251, "2": 7.090402454639255, "3": 0.8935451832375441, "4": 3.7889703531084735, "5": 2.3921256774649264, "6": 0.9916817703688188, "7": 2.583129029096832, "8": 6.828110271773845, "9": 2.571134714121467, "10": 9.468384560140903, "11": 10.525015459377139, "12": 7.210724827910421, "13": 0.9936511157275796, "14": 7.21274324798454, "15": 0.9939122848658316}, "Mean TTFT (ms)": {"0": 67.56553007098955, "1": 40.73448376399028, "2": 18316.767090197012, "3": 299.2719213240107, "4": 104.4357358600164, "5": 1196.684401954024, "6": 77.68955506602833, "7": 44484.592845969026, "8": 20066.769751820997, "9": 67523.52187434702, "10": 15274.585656341013, "11": 37767.74333799099, "12": 48086.013475898006, "13": 54.555806827005654, "14": 45785.34093497598, "15": 38.34820033599681}, "Median TTFT (ms)": {"0": 64.61613349983963, "1": 33.939811999971425, "2": 14784.63294500034, "3": 336.9845664992681, "4": 72.26192799953424, "5": 540.7159010001124, "6": 56.70144299983804, "7": 23836.06858299936, "8": 12178.349516999788, "9": 42070.8932109992, "10": 13725.114108000525, "11": 32781.61132349988, "12": 46735.81981949974, "13": 51.90685699972164, "14": 43124.55687850024, "15": 29.016246500077614}, "P99 TTFT (ms)": {"0": 102.22617789066132, "1": 136.14446343018244, "2": 46388.42228232968, "3": 833.6998585597574, "4": 248.42302643929466, "5": 7057.813544011041, "6": 151.38594406937005, "7": 157147.34324582896, "8": 55927.80764483006, "9": 221518.61635933968, "10": 33896.908273790694, "11": 82461.60382669978, "12": 106647.59210594019, "13": 107.84487404948777, "14": 111318.4520970504, "15": 94.74629583975457}, "Mean ITL (ms)": {"0": 27.803390078231295, "1": 11.924046373020358, "2": 142.72026268815387, "3": 246.19417273287524, "4": 36.835383122707185, "5": 347.8997794640821, "6": 22.932645166870877, "7": 366.4946344857622, "8": 136.22289588502997, "9": 367.1367094236028, "10": 107.67473392542954, "11": 105.74674683867245, "12": 143.67874235341387, "13": 15.78421428900555, "14": 135.13388223578633, "15": 8.603812842648303}, "Median ITL (ms)": {"0": 23.70899700008522, "1": 11.404827000205842, "2": 147.84702900033153, "3": 239.13052100033383, "4": 30.510911499732174, "5": 326.5406400005304, "6": 21.784756499982905, "7": 339.6840519999387, "8": 150.4070160003721, "9": 339.663931999894, "10": 122.18146400027763, "11": 137.1447060000719, "12": 144.94859499973245, "13": 14.822854499925597, "14": 147.05346949995146, "15": 8.302759999878617}, "P99 ITL (ms)": {"0": 103.7272884303911, "1": 27.108177600166538, "2": 474.56101334042626, "3": 312.6030967204133, "4": 137.3540552302072, "5": 641.4677220007433, "6": 58.52800169941474, "7": 639.7889072803081, "8": 293.17079524953436, "9": 643.244464719246, "10": 244.652573000167, "11": 191.63729379961296, "12": 409.87546703951926, "13": 51.74294369017843, "14": 187.65066829958414, "15": 16.065850999893893}}}
```

You can also check the raw experiment data in the Artifact tab of the Buildkite page.


