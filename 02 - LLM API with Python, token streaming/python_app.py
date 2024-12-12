import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('OPENAI_API_KEY') # It will automatically use the OPENAI_API_KEY from environment
if not api_key:
    raise ValueError("No OpenAI API key found. Please make sure OPENAI_API_KEY is set in your .env file")

# Initialize OpenAI client
client = OpenAI() 

def generate_blog_post(topic):
    """Generate a blog post using OpenAI API with streaming"""
    if not topic or len(topic.strip()) == 0:
        raise ValueError("Topic cannot be empty")

    try:
        # Create the prompt for blog post generation
        prompt = f"""Write a comprehensive blog post about {topic}. 
        The blog post should be well-structured with:
        - An engaging introduction
        - 3-4 main points with detailed explanations
        - Relevant examples or case studies
        - A strong conclusion
        - Proper headings and subheadings
        Please write in a professional yet conversational tone."""

        print(f"\nGenerating blog post about: {topic}")
        print("Streaming content...\n")

        # Create streaming completion
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional blog writer who creates engaging, well-researched content."},
                {"role": "user", "content": prompt}
            ],
            stream=True,
            temperature=0.7,
            max_tokens=2000
        )

        # Initialize content storage
        content = ""

        # Process the stream
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content_piece = chunk.choices[0].delta.content
                content += content_piece
                print(content_piece, end='', flush=True)

        if not content:
            raise ValueError("No content was generated")

        # Save the blog post
        save_blog_post(topic, content)
        return content

    except Exception as e:
        print(f"\nError generating blog post: {str(e)}")
        return None

def save_blog_post(topic, content):
    """Save the generated blog post to a file"""
    if not content:
        raise ValueError("Cannot save empty content")

    try:
        # Create a posts directory if it doesn't exist
        posts_dir = "generated_posts"
        if not os.path.exists(posts_dir):
            os.makedirs(posts_dir)

        # Create filename with sanitized topic
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{posts_dir}/blog_post_{sanitized_topic}_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {topic}\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(content)
        
        print(f"\n\nBlog post saved to {filename}")
        return filename
    except Exception as e:
        print(f"\nError saving blog post: {str(e)}")
        return None

def main():
    """Main function to run the blog post generator"""
    try:
        print("Welcome to the Blog Post Generator!")
        print("-----------------------------------")
        
        while True:
            topic = input("\nEnter the topic for your blog post (or 'quit' to exit): ").strip()
            
            if topic.lower() == 'quit':
                print("\nThank you for using the Blog Post Generator!")
                break
                
            if not topic:
                print("Please enter a valid topic.")
                continue
                
            generated_content = generate_blog_post(topic)
            
            if generated_content:
                print("\nBlog post generation completed successfully!")
            else:
                print("\nFailed to generate blog post. Please try again.")
                
            continue_writing = input("\nWould you like to generate another blog post? (y/n): ").strip().lower()
            if continue_writing != 'y':
                print("\nThank you for using the Blog Post Generator!")
                break

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    main()
