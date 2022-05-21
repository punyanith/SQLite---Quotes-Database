import sqlite3

# connect to the database
con = sqlite3.connect('quotes.db')
cur = con.cursor()

# create table if it does not already exists
cur.executescript('''
CREATE TABLE IF NOT EXISTS author(
    author_id INT PRIMARY KEY NOT NULL UNIQUE,
    f_name TEXT NOT NULL,
    l_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quotes(
    author_id INT NOT NULL,
    quote_id INT PRIMARY KEY NOT NULL UNIQUE,
    quote TEXT NOT NULL,
    FOREIGN KEY(author_id) REFERENCES author(author_id)
);
    
CREATE TABLE IF NOT EXISTS topic(
    topic_id INT PRIMARY KEY NOT NULL UNIQUE, 
    topic TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quote_has_topic(
    quote_id INT NOT NULL,
    topic_id INT NOT NULL,
    UNIQUE(quote_id, topic_id),
    PRIMARY KEY(quote_id, topic_id),
    FOREIGN KEY(quote_id) REFERENCES quotes(quote_id),
    FOREIGN KEY(topic_id) REFERENCES topic(topic_id)
);
''')

# Get the author_id to delete the author
def get_author(cur):
    cur.execute("SELECT author_id FROM author")
    results = cur.fetchall()
    if len(results) == 0:
        print("No quote in database")
        return None
    for i in range(len(results)):
        print(f"{i+1} - {results[i][0]}")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Author ID: "))
    return results[choice-1][0]


# Instruction
print("")
print("For the table to work and link together properly, ")
print("please input information into the table in the following order: ")
print("'Add New Author', 'Add New Quote', 'Add New Topic', and 'Link Quote ID with Topic ID'")
print("All of the above need to be done in order for the 'Display Quotes' to work.")
print("")


choice = None
while choice != "9":
    print("1) Add New Author")
    print("2) Display Author")
    print("3) Add New Quote")
    print("4) Add New Topic")
    print("5) Link Quote ID with Topic ID")
    print("6) Display Quotes")
    print("7) Update Quote's Topic")
    print("8) Delete Author")
    print("9) Quit")
    choice = input("> ")
    print()
    
    if choice == "1":
        try:
            # Add new author
            author_id = int(input("Author ID: "))
            f_name = input("Author First Name: ")
            l_name = input("Author Last Name: ")
            a = (author_id, f_name, l_name)
            cur.execute("INSERT INTO author VALUES (?,?,?)", a)    
            con.commit()
        except ValueError:
            print("Invalid Input")

    elif choice == "2":
        # Display author id, f_name, and l_name
        cur.execute("SELECT * FROM author")
        print("{:>10}   {:>10}   {:>10}".format("Author ID", " First", "Last"))
        for record in cur.fetchall():
            print("{:>10}   {:>10}   {:>10}".format(record[0], record[1], record[2]))

    elif choice == "3":
        # Add new quote
        try:
            q_author_id = int(input("Author ID: "))
            quote_id = int(input("Quote ID: "))
            quote = input("Quote: ")
            q = (q_author_id, quote_id, quote)
            cur.execute("INSERT INTO quotes VALUES (?,?,?)", q)
            con.commit()
        except ValueError:
            print("Invalid Input")

    elif choice == "4":
        # Add new topic
        try:
            topic_id = int(input("Topic ID: "))
            topic = input("Topic: ")
            t = (topic_id, topic)
            cur.execute("INSERT INTO topic VALUES (?,?)", t)
            con.commit()
        except ValueError:
            print("Invalid Input")

    elif choice == "5":
        # Link quote_id with topic_id
        try:
            l_quote_id = int(input("Quote ID: "))
            l_topic_id = int(input("Topic ID: "))
            qht = (l_quote_id, l_topic_id)
            cur.execute("INSERT INTO quote_has_topic VALUES (?,?)", qht)
            con.commit()
        except ValueError:
            print("Invalid Input")

    elif choice == "6":
        # Display  quote id, author id, topic id, topic, and quote
        cur.execute('''
        SELECT quote_has_topic.quote_id, author_id, quote_has_topic.topic_id, topic, quotes.quote
        FROM quotes
	    INNER JOIN quote_has_topic
		    ON quotes.quote_id = quote_has_topic.quote_id
	    INNER JOIN topic
		    ON quote_has_topic.topic_id = topic.topic_id
        ORDER BY quotes.quote_id;''')
        print("{:>10}   {:>10}  {:>10}  {:>10}  {:>10}".format("Quote ID", "Author ID", "Topic ID", "Topic", "Quote"))
        for record in cur.fetchall():
            print("{:>10}   {:>10}  {:>10}  {:>10}  {:>10}".format(record[0], record[1], record[2], record[3], record[4]))

    elif choice == "7":
        # Update Quote's Topic
        try:
            u_topic_id = input("Topic ID: ")
            u_quote_id = input("Quote ID: ")
            u_qht = (u_topic_id, u_quote_id)
            cur.execute("UPDATE quote_has_topic SET topic_id = ? WHERE quote_id = ?", u_qht)
            con.commit()
            if cur.rowcount == 0:
                print("Invalid quote ID")
        except ValueError:
            print("Invalid topic ID")

    elif choice == "8":
        # Delete author which will delete all the quotes from that author as well
        id = get_author(cur)
        if id == None:
            continue
        v = (id, )
        cur.execute("DELETE FROM quotes WHERE quotes.author_id = ?", v)
        cur.execute("DELETE FROM author WHERE author.author_id = ?", v)
        con.commit()
    print()

# Close the database connection before exiting
con.close()


# Topic 1 -- Life:
# q1. “The best thing to hold onto in life is each other.” — Audrey Hepburn


# Topic 2 -- Inspirational:
# q2. “Nothing is impossible. The word itself says ‘I’m possible’!” — Audrey Hepburn

# q3. “Be the change that you wish to see in the world.”― Mahatma Gandhi

# q4. “Beauty is everywhere. You only have to look to see it.” — Bob Ross


# Topic 3 -- Motivational:

# q5. “Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.” ― Roy Bennett

# q6. “It’s only after you’ve stepped outside your comfort zone that you begin to change, grow, and transform.” ― Roy Bennett

# Author:
# 1. Audrey Hepburn
# 2. Mahatma Gandhi
# 3. Bob Ross
# 4. Roy Bennett

