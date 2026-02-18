from collections import Counter
import re


regex_pattern = re.compile(r'\b[^\W\d_]+\b')  # Regular expression to match words (excluding numbers)
counter = Counter()
stop_words = set(["the", "a", "an", "and", "or", "to", "as",
                  "of", "in", "on", "for", "by", "with", "at",])
def main():
    with open("Anomolizer\\Windows_2k.log",'r') as file:
        
        # get each word count
        for line in file:
            words = re.findall(regex_pattern, line.lower()) 
            for word in words:
                if word.lower() not in stop_words:
                    counter[word] += 1
        
        total_entries = sum(counter.values())
        threshold = total_entries * 0.01  # 1% threshold
        # write the rare words occuring lines to a file
        with open("flagged_lines.txt", "w") as f:
            for word, count in counter.items():
                if count < threshold:
                    f.write(f"Word: {word}, Count: {count}\n")
        
        
if __name__ == "__main__":
    # print(lines)
    main()