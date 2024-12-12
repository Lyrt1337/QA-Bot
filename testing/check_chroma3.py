import chromadb
import matplotlib.pyplot as plt

# Initialize ChromaDB client
# client = chromadb.Client()
client = chromadb.PersistentClient(path=r"data\chroma")

# Specify the name of the collection
collection_name = "chroma_data"

# Retrieve the collection
collection = client.get_collection(collection_name)

# Fetch all documents in the collection
documents = collection.get()

# # Extract data for the histogram
# word_counts = []

# for doc in documents:
#     # Assuming each document has a "text" field
#     text = doc.get("text", "")
#     word_count = len(text.split())  # Count the number of words
#     word_counts.append(word_count)

# # Generate the histogram
# plt.figure(figsize=(10, 6))
# plt.hist(word_counts, bins=20, color='blue', edgecolor='black', alpha=0.7)
# plt.title("Word Count Distribution in ChromaDB Collection")
# plt.xlabel("Word Count")
# plt.ylabel("Frequency")
# plt.grid(axis='y', alpha=0.75)

# # Show the histogram
# plt.show()

print(documents)
