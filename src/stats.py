import json
import matplotlib.pyplot as plt
import pandas as pd

def analyze_serving_data(filename, remove_bad_rows=True):
    # load json file
    with open(filename, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame({
        'input_lens': data['input_lens'],
        'output_lens': data['output_lens'],
        'ttfts': data['ttfts'],
        'generated_texts': data['generated_texts'],
        'output_durations': [sum(latencies) for latencies in data['itls']]
    })
    # add additional columns:
    # - tokens: sum of input_lens and output_lens
    # - duration: ttft + sum(itl)
    # - tps: tokens / duration
    df['tokens'] = df['input_lens'] + df['output_lens']
    df['duration'] = df['ttfts'] + df['output_durations']
    df['tps'] = df['tokens'] / df['duration']
    df['tps_in'] = df['input_lens'] / df['ttfts']
    df['tps_out'] = df['output_lens'] / df['output_durations']

    # remove the bad rows
    if remove_bad_rows:
        df = df[(df['tokens'] > 4) & (df['output_lens'] > 2)]

    # Print the file name
    print(f"Analyzing file: {filename}")
    # Print the total number of samples
    print(f"  total samples: {len(df)}")
    print(f"  mean ttft: {df['ttfts'].mean()}")
    print(f"  mean itl: {df['output_durations'].mean()}")
    print(f"  mean tps: {df['tps_out'].mean()}")

    segments = {
        'short': df[df['tokens'] <= 100],
        'medium': df[(df['tokens'] > 100) & (df['tokens'] <= 500)],
        'long': df[df['tokens'] > 500]
    }
    for seg, df_seg in segments.items():
        print(f"  [{seg}] total samples: {len(df_seg)}")
        print(f"  [{seg}] mean tps: {df_seg['tps_out'].mean()}")

    return df


# plot a few diagrams
def plot_scatters(df_tee_on, df_tee_off, save_fig=''):
    fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 2))

    # Subplot 3: output_durations vs output_lengths
    ax3.scatter(df_tee_off['output_lens'], df_tee_off['output_durations'], alpha=0.3, color='blue', label='TEE-off', s=10)
    ax3.scatter(df_tee_on['output_lens'], df_tee_on['output_durations'], alpha=0.2, color='red', label='TEE-on', s=10)
    ax3.set_xlabel('Tokens Out')
    ax3.set_ylabel('Duration (s)')
    ax3.set_title('Duration vs Tokens Out')
    ax3.legend()

    # Subplot 4: tps vs Tokens
    ax4.scatter(df_tee_off['output_lens'], df_tee_off['tps_out'], alpha=0.3, color='blue', label='TEE-off', s=10)
    ax4.scatter(df_tee_on['output_lens'], df_tee_on['tps_out'], alpha=0.2, color='red', label='TEE-on', s=10)
    ax4.set_xlabel('Tokens Out')
    ax4.set_ylabel('TPS (tokens/s)')
    ax4.set_title('TPS vs Tokens Out')
    ax4.legend()

    plt.tight_layout()
    if save_fig:
        plt.savefig(save_fig, dpi=300)
    else:
        plt.show()


df_llama8b_off = analyze_serving_data('./results_base_llama8b_phi14b/serving_llama8B_tp1_sharegpt_qps_1.json')
df_llama8b_on = analyze_serving_data('./results_tee_serving_pass2/serving_llama8B_tp1_sharegpt_qps_1.json')

df_phi3_14b_off = analyze_serving_data('./results_base_llama8b_phi14b/serving_Phi3-14B-128k_tp1_sharegpt_qps_1.json')
df_phi3_14b_on = analyze_serving_data('./results_tee_serving_pass2/serving_Phi3-14B-128k_tp1_sharegpt_qps_1.json')

df_llama70b_off = analyze_serving_data('./results_base_llama70b/serving_llama70B_tp1_sharegpt_qps_1.json')
df_llama70b_on = analyze_serving_data('./results_tee_serving_pass2/serving_llama70B_tp1_sharegpt_qps_1.json')


# print the 10 rows with highest and lowest tps
print(df_llama70b_off.sort_values(by='tps', ascending=False).head(10))
print(df_llama70b_on.sort_values(by='tps', ascending=True).head(10))

plot_scatters(df_llama8b_on, df_llama8b_off, save_fig='./scatter-llama8b.png')
plot_scatters(df_phi3_14b_on, df_phi3_14b_off, save_fig='./scatter-phi14b.png')
plot_scatters(df_llama70b_on, df_llama70b_off, save_fig='./scatter-llama70b.png')
