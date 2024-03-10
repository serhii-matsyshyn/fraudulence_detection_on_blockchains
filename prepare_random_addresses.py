import random


def remove_duplicates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    print(len(lines))

    unique_lines = list(set(lines))

    return unique_lines

def subtract_lines(lines_file1, file2_path, output_path):
    with open(file2_path, 'r') as file2:
        lines_file2 = set(file2.readlines())

    result_lines = lines_file1 - lines_file2

    result_lines = ["ok," + line for line in result_lines]
    random.shuffle(result_lines)

    with open(output_path, 'w') as output_file:
        output_file.writelines(result_lines)

# Replace these paths with the actual paths of your input files and final output file
input_file1 = 'data/3_normal_addresses/interacted_addresses.txt'
input_file2 = 'data/2_data_collected/addresses_processed.txt'
final_output_file = 'data/3_normal_addresses/interacted_addresses_out.txt'

# Step 1: Remove duplicate lines from the first file
lines = remove_duplicates(input_file1)

print(len(lines))

# Step 2: Subtract lines from the second file and save the result in the final output file
subtract_lines(set(lines), input_file2, final_output_file)

# Print the number of lines in the final output file
with open(final_output_file, 'r') as final_output:
    num_lines = sum(1 for line in final_output)
    print(f"Number of lines after all steps: {num_lines}")