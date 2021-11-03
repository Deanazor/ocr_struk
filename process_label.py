import os, json, argparse

def main(args):
    label_raw = open(args.label, "r")
    label_lines = label_raw.readlines()
    lines = []
    for line in label_lines:
        fname, data = line.split("\t")
        if args.train:
            fname = os.path.join("train", fname.split("/")[-1])
        else:
            fname = os.path.join("test", fname.split("/")[-1])
        lines.append("{}\t{}".format(fname, data))
    
    with open(args.output, "w") as f:
        f.write("".join(line for line in lines))
        f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--label", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--train", action="store_true")

    args = parser.parse_args()
    main(args)
