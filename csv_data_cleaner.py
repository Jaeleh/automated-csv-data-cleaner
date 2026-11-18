import csv
import os


def create_sample_messy_csv(filename="messy_leads.csv"):
    """Creates a sample messy CSV file so you can test the script immediately."""
    sample_data = [
        ["Full Name", "Email", "Phone", "City"],
        ["  john doe  ", "JOHN.DOE@EXAMPLE.COM ", "876-555-0192", " kingston "],
        ["Jane Smith", "jane.smith@example.com", "876-555-0144", "Montego Bay"],
        ["  john doe  ", "JOHN.DOE@EXAMPLE.COM ", "876-555-0192", " kingston "],  # Duplicate
        ["", "", "", ""],  # Blank row
        ["mark brown", "invalid-email", "876-555-0188", "spanish town"],  # Bad email
        ["  SARAH LEE", "sarah.lee@example.com", "876-555-0177", "ocho rios  "],
    ]
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(sample_data)
    print(f"Created sample messy file: {filename}")


def clean_csv(input_file="messy_leads.csv", output_file="cleaned_leads.csv"):
    seen_records = set()
    cleaned_rows = []
    stats = {"total_read": 0, "blank_removed": 0, "duplicates_removed": 0, "invalid_emails": 0}

    with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        cleaned_rows.append([col.strip() for col in header])

        for row in reader:
            stats["total_read"] += 1

            # 1. Skip completely empty rows
            if not any(cell.strip() for cell in row):
                stats["blank_removed"] += 1
                continue

            # 2. Clean whitespace and standardize formatting
            name = row[0].strip().title()
            email = row[1].strip().lower()
            phone = row[2].strip()
            city = row[3].strip().title()

            # 3. Check for duplicate entries using email as unique key
            if email in seen_records:
                stats["duplicates_removed"] += 1
                continue
            seen_records.add(email)

            # 4. Flag invalid email addresses
            status = "Valid" if ("@" in email and "." in email) else "Needs Review"
            if status == "Needs Review":
                stats["invalid_emails"] += 1

            cleaned_rows.append([name, email, phone, city, status])

    # Add the new status column to the header
    cleaned_rows[0].append("Email Status")

    with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_rows)

    print("\n--- DATA CLEANING SUMMARY ---")
    print(f"Total rows processed : {stats['total_read']}")
    print(f"Blank rows removed   : {stats['blank_removed']}")
    print(f"Duplicates removed   : {stats['duplicates_removed']}")
    print(f"Invalid emails flagged: {stats['invalid_emails']}")
    print(f"Clean file saved to  : {os.path.abspath(output_file)}")


if __name__ == "__main__":
    create_sample_messy_csv()
    clean_csv()
