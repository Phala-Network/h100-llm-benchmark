
## Latency tests

- Input length: 32 tokens.
- Output length: 128 tokens.
- Batch size: fixed (8).
- Models: llama-3.1 8B, llama-3 70B, mixtral 8x7B.
- Evaluation metrics: end-to-end latency (mean, median, p99).


| Test name             | GPU   |   Mean latency (ms) |   Median latency (ms) |   P99 latency (ms) |
|:----------------------|:------|--------------------:|----------------------:|-------------------:|
| latency_gemma2-27b    | H200  |            2433.64  |              2433.01  |           2437.41  |
| latency_llama70B      | H200  |           28639     |             28640.4   |          28653.7   |
| latency_Phi3-14B-128k | H200  |            1605.72  |              1605     |           1608.65  |
| latency_llama8B       | H200  |             910.403 |               902.742 |            992.161 |


## Throughput tests

- Input length: randomly sample 200 prompts from ShareGPT dataset (with fixed random seed).
- Output length: the corresponding output length of these 200 prompts.
- Batch size: dynamically determined by vllm to achieve maximum throughput.
- Models: llama-3.1 8B, llama-3 70B, mixtral 8x7B.
- Evaluation metrics: throughput.


| Test name                | GPU   |   Tput (req/s) |
|:-------------------------|:------|---------------:|
| throughput_llama70B      | H200  |        2.18735 |
| throughput_Phi3-14B-128k | H200  |       12.8294  |
| throughput_llama8B       | H200  |       29.5973  |
| throughput_gemma2-27b    | H200  |       11.9303  |


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
| serving_Phi3-14B-128k_tp1_sharegpt_qps_4   | H200  |       3.83796  |          68.8304 |            66.2849 |        135.283  |        30.6977  |           25.6522 |       111.464  |
| serving_llama8B_tp1_sharegpt_qps_4         | H200  |       3.91684  |          36.8437 |            32.1393 |         80.7577 |        11.7723  |           10.854  |        25.2844 |
| serving_gemma27b_tp1_sharegpt_qps_16       | H200  |       6.1838   |       25536.2    |         17470.6    |      67451      |       171.524   |          188.938  |       376.065  |
| serving_llama70B_tp1_sharegpt_qps_1        | H200  |       0.893117 |         302.681  |           340.14   |        852.194  |       250.957   |          243.86   |       316.508  |
| serving_gemma27b_tp1_sharegpt_qps_4        | H200  |       3.79226  |         104.561  |            71.8571 |        415.285  |        39.0255  |           31.8077 |       144.068  |
| serving_llama70B_tp1_sharegpt_qps_4        | H200  |       2.33203  |        1776.37   |           606.136  |      11122.9    |       372.185   |          345.986  |       663.249  |
| serving_gemma27b_tp1_sharegpt_qps_1        | H200  |       0.992092 |          75.0639 |            53.2924 |        161.149  |        22.85    |           21.6343 |        58.6669 |
| serving_llama70B_tp1_sharegpt_qps_16       | H200  |       2.4886   |       46866.5    |         24580.3    |     166163      |       384.676   |          356.981  |       667.076  |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_16  | H200  |       5.71093  |       31674.5    |         23553      |      86356.4    |       169.992   |          195.208  |       350.885  |
| serving_llama70B_tp1_sharegpt_qps_inf      | H200  |       2.48074  |       69842.6    |         43688.7    |     230870      |       385.532   |          356.649  |       668.839  |
| serving_llama8B_tp1_sharegpt_qps_16        | H200  |       8.06336  |       20255.8    |         15506.6    |      45519.8    |       123.036   |           97.9871 |       239.899  |
| serving_llama8B_tp1_sharegpt_qps_inf       | H200  |       8.47542  |       47059.3    |         40964.9    |     102178      |       132.036   |          159.922  |       234.37   |
| serving_gemma27b_tp1_sharegpt_qps_inf      | H200  |       6.46171  |       51531.4    |         46896.1    |     122902      |       170.233   |          183.386  |       232.719  |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_1   | H200  |       0.994016 |          52.3634 |            49.4684 |        104.719  |        15.9645  |           15.0483 |        52.0941 |
| serving_Phi3-14B-128k_tp1_sharegpt_qps_inf | H200  |       6.09967  |       56121.7    |         52755.5    |     137335      |       164.527   |          184.499  |       242.647  |
| serving_llama8B_tp1_sharegpt_qps_1         | H200  |       0.994207 |          36.3674 |            27.0128 |         89.2463 |         8.71239 |            8.4196 |        16.6841 |


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
{"latency": {"Test name": {"0": "latency_gemma2-27b", "1": "latency_llama70B", "2": "latency_Phi3-14B-128k", "3": "latency_llama8B"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200"}, "Mean latency (ms)": {"0": 2433.644244600267, "1": 28639.025032266727, "2": 1605.7205620003515, "3": 910.4033824667567}, "Median latency (ms)": {"0": 2433.006701001432, "1": 28640.446904000783, "2": 1604.9982410004304, "3": 902.7419630001532}, "P99 latency (ms)": {"0": 2437.4122486203123, "1": 28653.71074461924, "2": 1608.649851320406, "3": 992.16065730041}}, "throughput": {"Test name": {"0": "throughput_llama70B", "1": "throughput_Phi3-14B-128k", "2": "throughput_llama8B", "3": "throughput_gemma2-27b"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200"}, "Tput (req/s)": {"0": 2.187350418846136, "1": 12.82939559993687, "2": 29.597279469926786, "3": 11.930327476798293}}, "serving": {"Test name": {"0": "serving_Phi3-14B-128k_tp1_sharegpt_qps_4", "1": "serving_llama8B_tp1_sharegpt_qps_4", "2": "serving_gemma27b_tp1_sharegpt_qps_16", "3": "serving_llama70B_tp1_sharegpt_qps_1", "4": "serving_gemma27b_tp1_sharegpt_qps_4", "5": "serving_llama70B_tp1_sharegpt_qps_4", "6": "serving_gemma27b_tp1_sharegpt_qps_1", "7": "serving_llama70B_tp1_sharegpt_qps_16", "8": "serving_Phi3-14B-128k_tp1_sharegpt_qps_16", "9": "serving_llama70B_tp1_sharegpt_qps_inf", "10": "serving_llama8B_tp1_sharegpt_qps_16", "11": "serving_llama8B_tp1_sharegpt_qps_inf", "12": "serving_gemma27b_tp1_sharegpt_qps_inf", "13": "serving_Phi3-14B-128k_tp1_sharegpt_qps_1", "14": "serving_Phi3-14B-128k_tp1_sharegpt_qps_inf", "15": "serving_llama8B_tp1_sharegpt_qps_1"}, "GPU": {"0": "H200", "1": "H200", "2": "H200", "3": "H200", "4": "H200", "5": "H200", "6": "H200", "7": "H200", "8": "H200", "9": "H200", "10": "H200", "11": "H200", "12": "H200", "13": "H200", "14": "H200", "15": "H200"}, "Tput (req/s)": {"0": 3.837956867952489, "1": 3.9168359805995907, "2": 6.183796212089202, "3": 0.8931172660813852, "4": 3.792263893844621, "5": 2.3320281994592826, "6": 0.9920919109762275, "7": 2.488599608868405, "8": 5.7109287461406835, "9": 2.480738504926752, "10": 8.06335857232855, "11": 8.475419201975813, "12": 6.461707110306633, "13": 0.9940164326647605, "14": 6.099665945296534, "15": 0.9942071837328349}, "Mean TTFT (ms)": {"0": 68.8304121209917, "1": 36.843746542002236, "2": 25536.209082524, "3": 302.68140134500663, "4": 104.56141779100744, "5": 1776.3682821439897, "6": 75.06391252798994, "7": 46866.491477300005, "8": 31674.53346650001, "9": 69842.562732765, "10": 20255.816553752993, "11": 47059.34656220601, "12": 51531.377914577024, "13": 52.36337209999806, "14": 56121.676371274996, "15": 36.36738758099824}, "Median TTFT (ms)": {"0": 66.28488149999612, "1": 32.13928849993408, "2": 17470.6191690002, "3": 340.1396105000458, "4": 71.8571110000994, "5": 606.136449499445, "6": 53.29238499984967, "7": 24580.294790000153, "8": 23553.038957000128, "9": 43688.732508499925, "10": 15506.629984500023, "11": 40964.94005299996, "12": 46896.080556499786, "13": 49.468427000192605, "14": 52755.498161999865, "15": 27.012761999969825}, "P99 TTFT (ms)": {"0": 135.2831589601101, "1": 80.75768578995392, "2": 67450.9619034096, "3": 852.1939450004811, "4": 415.2848586205982, "5": 11122.922920389981, "6": 161.14906866012893, "7": 166162.51628691936, "8": 86356.3740802404, "9": 230869.83321858986, "10": 45519.82591983994, "11": 102177.68647681011, "12": 122901.65670970002, "13": 104.71903155988002, "14": 137334.7772101899, "15": 89.24626619997183}, "Mean ITL (ms)": {"0": 30.697664912071232, "1": 11.772282235958984, "2": 171.52428055467144, "3": 250.95696224190655, "4": 39.025495340802806, "5": 372.18462432387815, "6": 22.850036070349237, "7": 384.67552587817676, "8": 169.99161096579564, "9": 385.5318922875249, "10": 123.03550933911679, "11": 132.03613486547238, "12": 170.23309675224127, "13": 15.964462636329516, "14": 164.5270365150945, "15": 8.712388674308547}, "Median ITL (ms)": {"0": 25.652209999861952, "1": 10.853974999918137, "2": 188.93756100032988, "3": 243.86005950009348, "4": 31.807653999749164, "5": 345.985634000499, "6": 21.634291000282246, "7": 356.98139400028595, "8": 195.20766750019902, "9": 356.64860600036263, "10": 97.98705399998653, "11": 159.9219390000144, "12": 183.38616949995412, "13": 15.048277999994752, "14": 184.4991515001766, "15": 8.419597999989037}, "P99 ITL (ms)": {"0": 111.46426953009266, "1": 25.284375799992674, "2": 376.0645694604676, "3": 316.50849762043435, "4": 144.0679835501213, "5": 663.2485065598667, "6": 58.66687005000127, "7": 667.0756011196863, "8": 350.8850285701282, "9": 668.8393058394377, "10": 239.89930980001193, "11": 234.36957780013475, "12": 232.71878259986804, "13": 52.094134429971746, "14": 242.64692306009235, "15": 16.684082600068006}}}
```

You can also check the raw experiment data in the Artifact tab of the Buildkite page.


