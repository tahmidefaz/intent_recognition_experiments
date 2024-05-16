import argparse
import glob
import yaml
import csv


def read_nlu_files(directory):
    nlu_files = glob.glob(directory + "/**/nlu.yml", recursive=True)
    intents = {}
    for file in nlu_files:
        with open(file, 'r') as f:
            if "/tours/nlu.yml" in file:
                continue

            data = yaml.safe_load(f)
            print("Filename: ", file)
            for item in data.get('nlu', []):
                intent = item.get('intent')
                examples = item.get('examples')
                if intent and examples:
                    examples = examples.split('\n')
                    examples = [example.strip("- ") for example in examples]
                    examples = [e for e in examples if len(e) > 0]
                    print("Intent:", intent)
                    print(examples)
                    write_to_csv(intent, examples)

    return intents

def write_to_csv(intent, examples):
    with open("output.csv", "a", newline='') as csvfile:
        fieldnames = ['intent', 'example']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        for example in examples:
            writer.writerow({'intent': intent, 'example': example})


def main():
    parser = argparse.ArgumentParser(description="Read and print intent examples from nlu.yml files")
    parser.add_argument("-d", "--directory", required=True, help="Path to directory containing nlu.yml files")
    args = parser.parse_args()

    directory = args.directory
    read_nlu_files(directory)
    print("done.")

if __name__ == "__main__":
    main()
