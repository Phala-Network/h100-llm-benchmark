
## Latency tests

- Input length: 32 tokens.
- Output length: 128 tokens.
- Batch size: fixed (8).
- Models: llama-3.1 8B, llama-3 70B, mixtral 8x7B.
- Evaluation metrics: end-to-end latency (mean, median, p99).


| Test name             | GPU   |   Mean latency (ms) |   Median latency (ms) |   P99 latency (ms) |
|:----------------------|:------|--------------------:|----------------------:|-------------------:|
| latency_gemma2-27b    | H200  |            2350.17  |              2350.16  |           2353.45  |
| latency_llama70B      | H200  |           28483.8   |             28483.1   |          28492.1   |
| latency_Phi3-14B-128k | H200  |            1544.63  |              1543.96  |           1548.06  |
| latency_llama8B       | H200  |             844.187 |               837.725 |            913.884 |


## Throughput tests

- Input length: randomly sample 200 prompts from ShareGPT dataset (with fixed random seed).
- Output length: the corresponding output length of these 200 prompts.
- Batch size: dynamically determined by vllm to achieve maximum throughput.
- Models: llama-3.1 8B, llama-3 70B, mixtral 8x7B.
- Evaluation metrics: throughput.


| Test name                | GPU   |   Tput (req/s) |
|:-------------------------|:------|---------------:|
| throughput_llama70B      | H200  |        2.20402 |
| throughput_Phi3-14B-128k | H200  |       13.8231  |
| throughput_llama8B       | H200  |       31.864   |
| throughput_gemma2-27b    | H200  |       12.413   |


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
| serving_Phi3-14B-128k_tp1_sharegpt_qps_4   | H200  |       3.85564  |          51.7481 |            48.5333 |         91.8261 |        23.7074  |          21.2741  |        75.8414 |
| serving_llama8B_tp1_sharegpt_qps_4         | H200  |       3.9241   |          28.2391 |            25.5211 |         54.8435 |         9.87139 |           9.71041 |        18.9339 |
| serving_gemma27b_tp1_sharegpt_qps_16       | H200  |       8.07153  |       11009.8    |          5107.26   |      29542.8    |       116.681   |         125.924   |       264.454  |
| serving_llama70B_tp1_sharegpt_qps_1        | H200  |       0.895576 |         297.315  |           338.859  |        831.205  |       243.004   |         235.948   |       309.166  |
| serving_gemma27b_tp1_sharegpt_qps_4        | H200  |       3.80226  |          87.9613 |            58.065  |        275.049  |        32.869   |          28.5268  |       115.151  |
| serving_llama70B_tp1_sharegpt_qps_4        | H200  |       2.41386  |        1154.12   |           545.612  |       6814.79   |       342.228   |         322.74    |       635.726  |
| serving_gemma27b_tp1_sharegpt_qps_1        | H200  |       0.992312 |          68.7075 |            46.3833 |        167.663  |        21.9642  |          20.9564  |        48.0012 |
| serving_llama70B_tp1_sharegpt_qps_16       | H200  |       2.61657  |       43996.9    |         23648.4    |     155666      |       362.657   |         335.601   |       635.03   |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_16  | H200  |       7.90778  |       13065.7    |          4861.03   |      38336.6    |       113.277   |         127.131   |       246.839  |
| serving_llama70B_tp1_sharegpt_qps_inf      | H200  |       2.61396  |       66645      |         43323.8    |     222375      |       361.155   |         334.529   |       639.153  |
| serving_llama8B_tp1_sharegpt_qps_16        | H200  |      11.4145   |       15144.4    |         18317.4    |      27473.5    |        39.8351  |          39.9162  |        80.2632 |
| serving_llama8B_tp1_sharegpt_qps_inf       | H200  |      12.4159   |       32901.1    |         28483.7    |      70149.3    |        89.1902  |          91.7751  |       169.073  |
| serving_gemma27b_tp1_sharegpt_qps_inf      | H200  |       8.45589  |       37009.1    |         35510.5    |      86164.7    |       118.661   |         123.973   |       185.167  |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_1   | H200  |       0.993969 |          42.5638 |            38.2406 |         87.5471 |        14.853   |          14.1679  |        37.4974 |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_inf | H200  |       8.38124  |       39588.5    |         36481.9    |      95837.1    |       116.583   |         126.977   |       173.327  |
| serving_llama8B_tp1_sharegpt_qps_1         | H200  |       0.994277 |          30.6677 |            22.7639 |         76.5181 |         7.86671 |           7.64937 |        12.8175 |


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
{"latency": {"Test name": {"0": "latency_gemma2-27b", "1": "latency_llama70B", "2": "latency_Phi3-14B-128k", "3": "latency_llama8B"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200"}, "Mean latency (ms)": {"0": 2350.1715415998965, "1": 28483.818934666728, "2": 1544.626435933363, "3": 844.1867786666382}, "Median latency (ms)": {"0": 2350.161213999854, "1": 28483.14112099979, "2": 1543.9604030007104, "3": 837.7254470005937}, "P99 latency (ms)": {"0": 2353.445376400523, "1": 28492.06811906024, "2": 1548.0611199003215, "3": 913.8837239199347}}, "throughput": {"Test name": {"0": "throughput_llama70B", "1": "throughput_Phi3-14B-128k", "2": "throughput_llama8B", "3": "throughput_gemma2-27b"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200"}, "Tput (req/s)": {"0": 2.2040183884497586, "1": 13.823091553663337, "2": 31.863977304985184, "3": 12.41303531279375}}, "serving": {"Test name": {"0": "serving_Phi3-14B-128k_tp1_sharegpt_qps_4", "1": "serving_llama8B_tp1_sharegpt_qps_4", "2": "serving_gemma27b_tp1_sharegpt_qps_16", "3": "serving_llama70B_tp1_sharegpt_qps_1", "4": "serving_gemma27b_tp1_sharegpt_qps_4", "5": "serving_llama70B_tp1_sharegpt_qps_4", "6": "serving_gemma27b_tp1_sharegpt_qps_1", "7": "serving_llama70B_tp1_sharegpt_qps_16", "8": "serving_Phi3-14B-128k_tp1_sharegpt_qps_16", "9": "serving_llama70B_tp1_sharegpt_qps_inf", "10": "serving_llama8B_tp1_sharegpt_qps_16", "11": "serving_llama8B_tp1_sharegpt_qps_inf", "12": "serving_gemma27b_tp1_sharegpt_qps_inf", "13": "serving_Phi3-14B-128k_tp1_sharegpt_qps_1", "14": "serving_Phi3-14B-128k_tp1_sharegpt_qps_inf", "15": "serving_llama8B_tp1_sharegpt_qps_1"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200", "4": "H200", "5": "H200", "6": "H200", "7": "H200", "8": "H200", "9": "H200", "10": "H200", "11": "H200", "12": "H200", "13": "H200", "14": "H200", "15": "H200"}, "Tput (req/s)": {"0": 3.8556353393374794, "1": 3.9240981008713613, "2": 8.07153064717606, "3": 0.8955758245465691, "4": 3.802259512811951, "5": 2.413859328489675, "6": 0.9923124193918679, "7": 2.616571443804678, "8": 7.907781902409165, "9": 2.613959214689794, "10": 11.414522966599307, "11": 12.415896815894069, "12": 8.455889416782883, "13": 0.993968733476544, "14": 8.381242459681133, "15": 0.9942769081057132}, "Mean TTFT (ms)": {"0": 51.748070970009394, "1": 28.23912960000007, "2": 11009.750233972014, "3": 297.31530176998785, "4": 87.96132521701747, "5": 1154.1152761600142, "6": 68.70746053498897, "7": 43996.927678273, "8": 13065.653509157008, "9": 66645.018843119, "10": 15144.397468716998, "11": 32901.050149994, "12": 37009.105801162994, "13": 42.56380538099552, "14": 39588.491472522, "15": 30.667743752996273}, "Median TTFT (ms)": {"0": 48.533345499890856, "1": 25.521140499904504, "2": 5107.2635380000975, "3": 338.85882999993555, "4": 58.06500649987356, "5": 545.6119969999236, "6": 46.38334300011593, "7": 23648.43890899965, "8": 4861.0334019999755, "9": 43323.81855450012, "10": 18317.383314499923, "11": 28483.651113999942, "12": 35510.49047350034, "13": 38.240589999986696, "14": 36481.90318799993, "15": 22.763913499943556}, "P99 TTFT (ms)": {"0": 91.82613088003563, "1": 54.84347266994064, "2": 29542.786501959297, "3": 831.2049937399113, "4": 275.0489224600179, "5": 6814.78992143976, "6": 167.66344311997221, "7": 155665.5789246805, "8": 38336.6111409802, "9": 222374.79190342067, "10": 27473.452360940173, "11": 70149.31522050984, "12": 86164.65957773071, "13": 87.54707858015536, "14": 95837.13711913985, "15": 76.51810743997203}, "Mean ITL (ms)": {"0": 23.707366900802242, "1": 9.871389655653239, "2": 116.68131587554375, "3": 243.00382693496329, "4": 32.86896264641211, "5": 342.2283196599496, "6": 21.96422450759447, "7": 362.6569936725173, "8": 113.27728813091949, "9": 361.15454938076, "10": 39.83508714881614, "11": 89.19022317519457, "12": 118.66145929102117, "13": 14.853048088809516, "14": 116.58251227102257, "15": 7.866706498748347}, "Median ITL (ms)": {"0": 21.274061999974947, "1": 9.710412000003998, "2": 125.92362800069168, "3": 235.94821099959518, "4": 28.526795000288985, "5": 322.73974000054295, "6": 20.956363000095735, "7": 335.60111399947345, "8": 127.13149449996308, "9": 334.52854550023403, "10": 39.91624300010699, "11": 91.77511600000798, "12": 123.97250349977185, "13": 14.16789199993218, "14": 126.97670250008741, "15": 7.64936900009161}, "P99 ITL (ms)": {"0": 75.84144895992713, "1": 18.93394419994366, "2": 264.4538787303102, "3": 309.1660043802585, "4": 115.15140490967492, "5": 635.7259346101275, "6": 48.00116120027269, "7": 635.0302084997566, "8": 246.8387429498989, "9": 639.1528507894236, "10": 80.26316299997234, "11": 169.07301859996554, "12": 185.16704092947293, "13": 37.49742118003269, "14": 173.32669017998793, "15": 12.817478599936301}}}
```

You can also check the raw experiment data in the Artifact tab of the Buildkite page.


