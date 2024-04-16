# Last Modified April 2024
# Brune Bettler

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import numpy as np
import scipy
import seaborn as sns
from data_loader import *

def see_ER_length(length_data, worm_label, save=False):
    x = np.arange((len(length_data)))
    pump_num = len(length_data)

    plt.scatter(x, length_data)
    plt.title(f'E to R Peak Distance for {worm_label}')
    plt.xlabel("Pump Number")
    plt.ylabel("Distance Between E and R Peaks (sec)")
    annotation_text = f'n = {pump_num}'
    ax = plt.gca()
    plt.text(0.90, 0.97, annotation_text, va='top', ha='left', transform=ax.transAxes, fontsize=8)

    if save:
        plt.savefig(f"ER Peak Distance for {worm_label}.png")
    plt.show()

    return 0

def see_RE_distance(distance_data, worm_label, save=False):
    x = np.arange((len(distance_data)))
    pump_num = len(distance_data)

    plt.scatter(x, distance_data)
    plt.title(f'Previous R to Next E Peak Distance for {worm_label}')
    plt.xlabel("Gap Number")
    plt.ylabel("Gap Distance (sec)")
    annotation_text = f'n = {pump_num}'
    ax = plt.gca()
    plt.text(0.90, 0.97, annotation_text, va='top', ha='left', transform=ax.transAxes, fontsize=8)

    if save:
        plt.savefig(f"RE Gap Distance for {worm_label}.png")
    plt.show()

    return 0

def stats(data, worm_id):
    mean = np.mean(data)
    std_dev = np.std(data)
    variance = np.var(data)
    median = np.median(data)
    range_data = np.ptp(data)  # (max - min)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    skewness = scipy.stats.skew(data)
    kurtosis = scipy.stats.kurtosis(data)

    # Display the results
    print('Worm num: ', worm_id)
    print("Mean:", mean)
    print("Standard Deviation:", std_dev)
    print("Variance:", variance)
    print("Median:", median)
    print("Range:", range_data)
    print("IQR:", iqr)
    print("Skewness:", skewness)
    print("Kurtosis:", kurtosis)

    return mean

def length_histogram(all_length_data, all_worm_labels=None, save=False):
    for i, worm_l_data in enumerate(all_length_data):
        sns.kdeplot(worm_l_data, label=all_worm_labels[i])

    plt.title(f'Kernel Density Estimate Plot for E to R Peak Distance \n MT Control Worms')
    plt.legend()
    plt.xlabel('E to R Peak Distance (sec)')
    plt.ylabel('Density')

    if save:
        plt.savefig(f"KDE plot for all MT control worms.png")

    plt.show()
    return 0

def distance_histogram(all_distance_data, all_worm_labels=None, save=False):
    for i, worm_d_data in enumerate(all_distance_data):
        sns.kdeplot(worm_d_data, label=all_worm_labels[i])

    plt.title(f'Kernel Density Estimate Plot for R to E Peak Distance (Gaps) \n MT Control Worms')
    plt.legend()
    plt.xlabel('R to E Gap Distance (sec)')
    plt.ylabel('Density')

    if save:
        plt.savefig(f"RE Gap KDE plot for all MT control worms.png")

    plt.show()
    return 0

def see_h202_plots(pre_length, post_length, pre_distance, post_distance, worm_label=None, save=False):
    plt.figure(figsize=(10, 5))
    plt.suptitle(f"Pre and Post H2O2 Addition \n{worm_label}")

    # plot ER length pre and post
    plt.subplot(1, 2, 1)
    sig_len = mannwhitneyu(pre_length, post_length)
    plt.scatter(np.arange(len(pre_length)), pre_length, color='blue', label=f'Pre H2O2 | n={len(pre_length)}')
    plt.scatter(np.arange(len(post_length)), post_length, color='red', label=f'Post H2O2 | n={len(post_length)}')
    plt.title(f'E to R Peak Length \np={sig_len.pvalue}')
    plt.xlabel('Spike Number')
    plt.ylabel('E to R Length (sec)')
    plt.legend()

    # Second subplot
    plt.subplot(1, 2, 2)
    sig_dist = mannwhitneyu(pre_distance, post_distance)
    plt.scatter(np.arange(len(pre_distance)), pre_distance, color='blue', label=f'Pre H2O2 | n={len(pre_distance)}')
    plt.scatter(np.arange(len(post_distance)), post_distance, color='red', label=f'Post H2O2 | n={len(post_distance)}')
    plt.title(f'R to E Gap Distance \np={round(sig_dist.pvalue, 3)}')
    plt.xlabel('Gap number')
    plt.ylabel('R to E Gap Distance (sec)')
    plt.legend()

    plt.tight_layout()  # Adjusts subplots to give some padding between them

    if save:
        plt.savefig(f"{worm_label} duo plot.png")

    plt.show()

    return 0

def H202_hist_plots(pre_length, post_length, pre_distance, post_distance, worm_label=None, save=False):
    plt.figure(figsize=(10, 5))
    plt.suptitle(f"Pre and Post H2O2 Addition Kernel Density Estimate Plots \n{worm_label}")

    # plot ER length pre and post
    plt.subplot(1, 2, 1)
    #sig_len = mannwhitneyu(pre_length, post_length)
    sns.histplot(pre_length, stat='frequency', label=f'Pre H2O2 | n={len(pre_length)}', color="blue", edgecolor=None, alpha=0.3)
    sns.histplot(post_length, stat='frequency', label=f'Post H2O2 | n={len(post_length)}', color="red", edgecolor=None, alpha=0.3)

    plt.title(f'E to R Peak Length')
    plt.xlabel('E to R Length (sec)')
    plt.ylabel('Frequency')
    plt.legend()

    # Second subplot
    plt.subplot(1, 2, 2)
    #sig_dist = mannwhitneyu(pre_distance, post_distance)
    sns.histplot(pre_distance, stat='frequency', label=f'Pre H2O2 | n={len(pre_length)}', color="blue", edgecolor=None, alpha=0.3)
    sns.histplot(post_distance, stat='frequency', label=f'Post H2O2 | n={len(post_length)}', color="red", edgecolor=None, alpha=0.3)

    plt.title(f'R to E Gap Distance')
    plt.xlabel('R to E Gap Distance (sec)')
    plt.ylabel('Frequency')
    plt.legend()

    plt.tight_layout()  # Adjusts subplots to give some padding between them

    if save:
        plt.savefig(f"{worm_label} HISTOGRAM duo plot.png")

    plt.show()

    return 0

def get_frequency_data(ER_spike_times):
    # Overall frequency calculation
    total_time = ER_spike_times[-1][0] - ER_spike_times[0][0]  # Duration from first to last spike
    total_spikes = len(ER_spike_times)
    overall_frequency = total_spikes / total_time

    # Frequency over smaller intervals
    bin_seconds = 10
    time_bins = np.arange(ER_spike_times[0][0], ER_spike_times[-1][0], bin_seconds)
    bin_counts = np.histogram(ER_spike_times, bins=time_bins)[0]
    if len(bin_counts) == 0:
        bin_counts = 1

    frequencies = bin_counts / (total_time/len(time_bins))
    mean = round(np.mean(np.array(frequencies)), 2)
    frequencies = np.round(frequencies, 2)

    print("mean", mean)
    print("Frequencies over time:", frequencies, "Hz")

    return mean, np.array(frequencies)

def plot_freq_data(all_mean_freq, all_interval_freq, worm_labels, worm_type_title, save=False):
    plt.figure(figsize=(10, 5))
    colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","beige","brown","gray","cyan","magenta"])
    plt.suptitle(f"Pump Frequency\n{worm_type_title}")

    # plot mean frequency for all worms
    plt.subplot(1, 2, 1)
    x = np.arange(len(all_mean_freq))
    y = all_mean_freq
    plt.scatter(x,y,c=colors[:len(x)])
    plt.title(f'Mean Pump Frequencies')
    plt.xlabel('Worm Number')
    plt.ylabel('Pump Frequency')

    # Second subplot
    plt.subplot(1, 2, 2)
    for i, worm_data in enumerate(all_interval_freq):
        x = np.arange(len(all_interval_freq[i]))
        y = worm_data
        c = colors[i]
        l = worm_labels[i]
        plt.plot(x,y,c=c, label=l)

    plt.title(f'Frequency Over Time')
    plt.xlabel('Bin Number (10 seconds each)')
    plt.ylabel('Mean Pump Frequency')
    plt.legend()

    plt.tight_layout()

    if save:
        plt.savefig(f"WT Control Worms Frequency plot.png")

    plt.show()

    return 0

def freq_H2O2_vs_control(all_freq_postH2O2, all_freq_control, save=False):
    # histogram of all control vs all mutant combined
    # combine all_freq for both into single np array

    sns.histplot(all_freq_postH2O2, color="red", stat='frequency', label=f'WT Post H2O2 | n={len(all_freq_postH2O2)} freq from n=4 worms', edgecolor=None, alpha=0.3)
    sns.histplot(all_freq_control, color="blue", stat='frequency', label=f'WT Control | n={len(all_freq_control)} freq from n=8 worms', edgecolor=None, alpha=0.3)
    plt.legend()
    plt.title("Pump Frequency Histogram post H2O2 vs Control \n in WT Worms")
    plt.xlabel("Pump Frequency (calculated over 10s ranges)")

    plt.savefig("WT postH2O2 vs Control histogram.png")
    plt.show()

    return 0

def box_H2o2_vs_control(all_freq_postH2O2, all_freq_control, save=False):
    data = [all_freq_control, all_freq_postH2O2]
    plt.boxplot(data)
    plt.ylabel('Pump Frequency (Per 10 second bin)')
    plt.xticks([1, 2], ['WT Control', 'WT Post H2O2'])  # Label x-ticks for clarity
    plt.title("Pump Frequency in WT Control Worms vs Post H2O2 Worms")
    plt.savefig("pump freq box WT.png")
    plt.show()

if __name__ == '__main__':
   print("test here")







