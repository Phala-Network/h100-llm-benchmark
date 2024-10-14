import json
import matplotlib.pyplot as plt
import pandas as pd
import os

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

    # Calculate metrics once
    total_samples = len(df)
    mean_ttft = df['ttfts'].mean()
    mean_itl = df['output_durations'].mean()
    mean_tps = df['tps_out'].mean()

    csv_row = [
        filename,
        total_samples,
        mean_ttft,
        mean_itl,
        mean_tps
    ]

    # Print the file name
    print(f"Analyzing file: {filename}")
    # Print the total number of samples
    print(f"  total samples: {total_samples}")
    print(f"  mean ttft: {mean_ttft}")
    print(f"  mean itl: {mean_itl}")
    print(f"  mean tps: {mean_tps}")

    segments = {
        'short': df[df['tokens'] <= 100],
        'medium': df[(df['tokens'] > 100) & (df['tokens'] <= 500)],
        'long': df[df['tokens'] > 500]
    }
    for seg, df_seg in segments.items():
        seg_samples = len(df_seg)
        seg_mean_tps = df_seg['tps_out'].mean()
        csv_row.extend([seg_samples, seg_mean_tps])
        print(f"  [{seg}] total samples: {seg_samples}")
        print(f"  [{seg}] mean tps: {seg_mean_tps}")

    return df, csv_row


# plot a few diagrams
def plot_scatters(df_tee_on, df_tee_off, output_dir, model_name):
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
    save_fig = os.path.join(output_dir, f'scatter-{model_name}.png')
    plt.savefig(save_fig, dpi=300)
    plt.close()  # Close the figure to free up memory

def combine_csv(rows, output_dir):
    BASE_HEAD = ['filename', 'total_samples', 'ttft', 'itl', 'tps', 'short_total', 'short_tps', 'medium_total', 'medium_tps', 'long_total', 'long_tps']
    HEAD = []
    for column in BASE_HEAD:
        HEAD.extend([f'{column}_tee_on', f'{column}_tee_off'])
    
    lines = [','.join(HEAD)]
    for i in range(len(rows) // 2):  # Use integer division
        row = []
        for j in range(len(rows[0])):
            row.append(str(rows[2*i][j]))
            row.append(str(rows[2*i+1][j]))
        lines.append(','.join(row))
    
    filename = os.path.join(output_dir, 'combined_results.csv')
    with open(filename, 'w') as fout:
        for l in lines:
            fout.write(l)
            fout.write('\n')

# Add a new function to create the output directory if it doesn't exist
def ensure_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# Update the main execution block
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze serving data and generate plots.")
    parser.add_argument("--output_dir", default="./outputs/out1", help="Directory to save output files")
    args = parser.parse_args()

    output_dir = ensure_output_dir(args.output_dir)

    df_llama8b_off, csv_llama8b_off = analyze_serving_data('./results/base_24cores/serving_llama8B_tp1_sharegpt_qps_1.json')
    df_llama8b_on, csv_llama8b_on = analyze_serving_data('./results/tee_24cores/serving_llama8B_tp1_sharegpt_qps_1.json')

    df_phi3_14b_off, csv_phi3_14b_off = analyze_serving_data('./results/base_24cores/serving_Phi3-14B-128k_tp1_sharegpt_qps_1.json')
    df_phi3_14b_on, csv_phi3_14b_on = analyze_serving_data('./results/tee_24cores/serving_Phi3-14B-128k_tp1_sharegpt_qps_1.json')

    df_llama70b_off, csv_llama70b_off = analyze_serving_data('./results/base_24cores/serving_llama70B_tp1_sharegpt_qps_1.json')
    df_llama70b_on, csv_llama70b_on = analyze_serving_data('./results/tee_24cores/serving_llama70B_tp1_sharegpt_qps_1.json')

    # print the 10 rows with highest and lowest tps
    print(df_llama70b_off.sort_values(by='tps', ascending=False).head(10))
    print(df_llama70b_on.sort_values(by='tps', ascending=True).head(10))

    plot_scatters(df_llama8b_on, df_llama8b_off, output_dir, 'llama8b')
    plot_scatters(df_phi3_14b_on, df_phi3_14b_off, output_dir, 'phi14b')
    plot_scatters(df_llama70b_on, df_llama70b_off, output_dir, 'llama70b')

    combine_csv([csv_llama8b_on, csv_llama8b_off, csv_phi3_14b_on, csv_phi3_14b_off, csv_llama70b_on, csv_llama70b_off], output_dir)