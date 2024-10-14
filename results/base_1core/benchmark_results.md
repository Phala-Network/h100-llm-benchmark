
## Latency tests

- Input length: 32 tokens.
- Output length: 128 tokens.
- Batch size: fixed (8).
- Models: llama-3.1 8B, llama-3 70B, mixtral 8x7B.
- Evaluation metrics: end-to-end latency (mean, median, p99).


| Test name             | GPU   |   Mean latency (ms) |   Median latency (ms) |   P99 latency (ms) |
|:----------------------|:------|--------------------:|----------------------:|-------------------:|
| latency_gemma2-27b    | H200  |             2349.84 |              2349.3   |           2353.98  |
| latency_llama70B      | H200  |            28456.4  |             28455.9   |          28467.6   |
| latency_Phi3-14B-128k | H200  |             1542.39 |              1541.99  |           1544.49  |
| latency_llama8B       | H200  |              841.53 |               835.413 |            908.952 |


## Throughput tests

- Input length: randomly sample 200 prompts from ShareGPT dataset (with fixed random seed).
- Output length: the corresponding output length of these 200 prompts.
- Batch size: dynamically determined by vllm to achieve maximum throughput.
- Models: llama-3.1 8B, llama-3 70B, mixtral 8x7B.
- Evaluation metrics: throughput.


| Test name                | GPU   |   Tput (req/s) |
|:-------------------------|:------|---------------:|
| throughput_llama70B      | H200  |        2.20112 |
| throughput_Phi3-14B-128k | H200  |       13.8558  |
| throughput_llama8B       | H200  |       32.0134  |
| throughput_gemma2-27b    | H200  |       12.4566  |


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
| serving_Phi3-14B-128k_tp1_sharegpt_qps_4   | H200  |       3.85774  |          50.7543 |            47.1288 |         86.6562 |        24.3312  |          20.488   |        78.0751 |
| serving_llama8B_tp1_sharegpt_qps_4         | H200  |       3.92398  |          28.3125 |            25.2541 |         57.0512 |        10.1673  |           9.61202 |        20.2839 |
| serving_gemma27b_tp1_sharegpt_qps_16       | H200  |       7.18321  |       17707.1    |          9993.85   |      47574.8    |       143.199   |         157.567   |       308.391  |
| serving_llama70B_tp1_sharegpt_qps_1        | H200  |       0.895302 |         292.113  |           331.952  |        829.53   |       245.069   |         237.589   |       312.767  |
| serving_gemma27b_tp1_sharegpt_qps_4        | H200  |       3.80449  |          89.5617 |            57.4438 |        376.349  |        34.3561  |          28.4418  |       118.984  |
| serving_llama70B_tp1_sharegpt_qps_4        | H200  |       2.39447  |        1275.34   |           561.473  |       7545.62   |       350.213   |         329.176   |       642.301  |
| serving_gemma27b_tp1_sharegpt_qps_1        | H200  |       0.992555 |          67.618  |            44.6553 |        170.424  |        21.9652  |          20.9182  |        49.211  |
| serving_llama70B_tp1_sharegpt_qps_16       | H200  |       2.57965  |       44322.3    |         23587      |     157179      |       368.884   |         341.027   |       646.18   |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_16  | H200  |       6.76799  |       21968.6    |         13209.5    |      61709.2    |       139.783   |         160.585   |       291.068  |
| serving_llama70B_tp1_sharegpt_qps_inf      | H200  |       2.57458  |       67614.5    |         42685.5    |     222001      |       366.442   |         339.808   |       647.052  |
| serving_llama8B_tp1_sharegpt_qps_16        | H200  |       9.68124  |       17766.2    |         19562.8    |      32398.2    |        75.6359  |          62.4664  |       147.562  |
| serving_llama8B_tp1_sharegpt_qps_inf       | H200  |       9.97817  |       40292.2    |         36353.6    |      86094.3    |       111.408   |          92.5542  |       210.808  |
| serving_gemma27b_tp1_sharegpt_qps_inf      | H200  |       7.57385  |       43934.9    |         40859.7    |     104501      |       144.142   |         154.35    |       204.303  |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_1   | H200  |       0.994161 |          41.6916 |            37.8191 |         85.2209 |        14.9387  |          14.2798  |        38.3932 |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_inf | H200  |       7.20749  |       47792.3    |         44964.3    |     116575      |       138.494   |         155.285   |       208.846  |
| serving_llama8B_tp1_sharegpt_qps_1         | H200  |       0.994429 |          30.0681 |            22.1734 |         74.5161 |         7.89701 |           7.65914 |        12.4538 |


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
{"latency": {"Test name": {"0": "latency_gemma2-27b", "1": "latency_llama70B", "2": "latency_Phi3-14B-128k", "3": "latency_llama8B"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200"}, "Mean latency (ms)": {"0": 2349.8381820666814, "1": 28456.40620079994, "2": 1542.3916868000258, "3": 841.5303283999796}, "Median latency (ms)": {"0": 2349.3020229998365, "1": 28455.909498999972, "2": 1541.9904000000315, "3": 835.4132390004452}, "P99 latency (ms)": {"0": 2353.9833086603358, "1": 28467.557954479817, "2": 1544.4921562999116, "3": 908.9520248606459}}, "throughput": {"Test name": {"0": "throughput_llama70B", "1": "throughput_Phi3-14B-128k", "2": "throughput_llama8B", "3": "throughput_gemma2-27b"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200"}, "Tput (req/s)": {"0": 2.201119305193731, "1": 13.855819717212373, "2": 32.013448236994606, "3": 12.456604142603647}}, "serving": {"Test name": {"0": "serving_Phi3-14B-128k_tp1_sharegpt_qps_4", "1": "serving_llama8B_tp1_sharegpt_qps_4", "2": "serving_gemma27b_tp1_sharegpt_qps_16", "3": "serving_llama70B_tp1_sharegpt_qps_1", "4": "serving_gemma27b_tp1_sharegpt_qps_4", "5": "serving_llama70B_tp1_sharegpt_qps_4", "6": "serving_gemma27b_tp1_sharegpt_qps_1", "7": "serving_llama70B_tp1_sharegpt_qps_16", "8": "serving_Phi3-14B-128k_tp1_sharegpt_qps_16", "9": "serving_llama70B_tp1_sharegpt_qps_inf", "10": "serving_llama8B_tp1_sharegpt_qps_16", "11": "serving_llama8B_tp1_sharegpt_qps_inf", "12": "serving_gemma27b_tp1_sharegpt_qps_inf", "13": "serving_Phi3-14B-128k_tp1_sharegpt_qps_1", "14": "serving_Phi3-14B-128k_tp1_sharegpt_qps_inf", "15": "serving_llama8B_tp1_sharegpt_qps_1"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200", "4": "H200", "5": "H200", "6": "H200", "7": "H200", "8": "H200", "9": "H200", "10": "H200", "11": "H200", "12": "H200", "13": "H200", "14": "H200", "15": "H200"}, "Tput (req/s)": {"0": 3.857740620629476, "1": 3.9239751247774697, "2": 7.183212170646673, "3": 0.8953018860583619, "4": 3.804487654311555, "5": 2.394465240184031, "6": 0.9925545555910471, "7": 2.579654312513955, "8": 6.767992947506282, "9": 2.5745776456948133, "10": 9.681238105999416, "11": 9.978165145714007, "12": 7.573851453947267, "13": 0.9941608052154389, "14": 7.2074911703078754, "15": 0.9944285629531834}, "Mean TTFT (ms)": {"0": 50.754269692996786, "1": 28.312460488997885, "2": 17707.069438673007, "3": 292.112833397995, "4": 89.56170344500515, "5": 1275.3361906269984, "6": 67.61800212099706, "7": 44322.295086665006, "8": 21968.619250731, "9": 67614.453342612, "10": 17766.185866529006, "11": 40292.224646587994, "12": 43934.86509907098, "13": 41.69158301899097, "14": 47792.253760322994, "15": 30.068141110000624}, "Median TTFT (ms)": {"0": 47.12877299994034, "1": 25.254057499978444, "2": 9993.847521000134, "3": 331.9521104995147, "4": 57.44382799957748, "5": 561.4732389999517, "6": 44.655275499962954, "7": 23586.97981450041, "8": 13209.500535000188, "9": 42685.51186100012, "10": 19562.83805999999, "11": 36353.6112354999, "12": 40859.719892000154, "13": 37.81906949984659, "14": 44964.26880150011, "15": 22.17337350001003}, "P99 TTFT (ms)": {"0": 86.65617979971557, "1": 57.05123775011088, "2": 47574.80036672013, "3": 829.5298184005605, "4": 376.3489962703623, "5": 7545.6172396301645, "6": 170.42386078987843, "7": 157179.21983139025, "8": 61709.15180544969, "9": 222000.81804350033, "10": 32398.19897016998, "11": 86094.26974127011, "12": 104500.75534315032, "13": 85.22086060002037, "14": 116575.06020504999, "15": 74.51610572000845}, "Mean ITL (ms)": {"0": 24.331204982133652, "1": 10.167328458822675, "2": 143.19905740985936, "3": 245.06872415164037, "4": 34.356080289367114, "5": 350.21300101892064, "6": 21.965234535267268, "7": 368.88352677902986, "8": 139.78332522345949, "9": 366.4417854705919, "10": 75.63592622916002, "11": 111.40812223625348, "12": 144.14245729075282, "13": 14.938679930188082, "14": 138.49389051707624, "15": 7.897011684788837}, "Median ITL (ms)": {"0": 20.488030500018795, "1": 9.61201599989181, "2": 157.5671885002521, "3": 237.58871449990693, "4": 28.44180400006735, "5": 329.1761730001781, "6": 20.918234999726337, "7": 341.0266170003524, "8": 160.5847220000669, "9": 339.8084899999958, "10": 62.46644400016521, "11": 92.554231999884, "12": 154.3502089998583, "13": 14.279789000056553, "14": 155.28502400002253, "15": 7.6591439999447175}, "P99 ITL (ms)": {"0": 78.07513040009778, "1": 20.28394140011187, "2": 308.3912572094503, "3": 312.7672247096962, "4": 118.98448550055033, "5": 642.3012803804613, "6": 49.21099558003789, "7": 646.1801673200534, "8": 291.0682785997687, "9": 647.0523570998012, "10": 147.56214400003958, "11": 210.8084950000375, "12": 204.3029024404314, "13": 38.393171530078675, "14": 208.84649204004288, "15": 12.45382939998763}}}
```

You can also check the raw experiment data in the Artifact tab of the Buildkite page.


