import openai
import csv
import os

# Authenticate with OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")


def analyze_review(review):
    # Use OpenAI's GPT-3 to evaluate sentiment of review
    prompt = "Please evaluate the sentiment of the following review on a scale of 1 to 10:\n\n" + review + "\n\nScore:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )
    sentiment_score = int(float(response.choices[0].text.strip()))

    return sentiment_score


def analyze_reviews(input_filename):
    # Read reviews from CSV file
    reviews = []
    with open(input_filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        for row in csv_reader:
            print(row)
            reviews.append(row)

    # Analyze sentiment of each review
    for review in reviews:
        sentiment_score = analyze_review(review['review text'])
        review['rate'] = sentiment_score

    # Sort reviews by sentiment score in descending order
    reviews.sort(key=lambda x: x['rate'], reverse=True)

    # Write analyzed reviews to new CSV file
    output_filename = os.path.splitext(input_filename)[0] + '_analyzed.csv'
    with open(output_filename, 'w', newline='') as csv_file:
        fieldnames = ['email', 'rate']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for review in reviews:
            csv_writer.writerow({'email': review['email'], 'rate': review['rate']})

    print(f'Successfully analyzed {len(reviews)} reviews and wrote result to {output_filename}.')


if __name__ == '__main__':
    input_filename = 'review/data1.csv'
    analyze_reviews(input_filename)
