"""
Example usage of PreProcessing singleton
This file demonstrates how to use the PreProcessing instance from anywhere in the application
"""

# Method 1: Using the global instance
from app.core.globals import get_global_preprocessing

def example_using_global():
    """Example using global preprocessing instance"""
    preprocessing = get_global_preprocessing()
    
    # Test text processing
    test_text = "Đây là một văn bản tiếng Việt để test preprocessing."
    processed_text = preprocessing.text_preprocessing_vietnamese(test_text)
    
    print(f"Original: {test_text}")
    print(f"Processed: {processed_text}")
    
    return processed_text

# Method 2: Using the singleton directly
from app.utils.preprocessing_singleton import get_preprocessing

def example_using_singleton():
    """Example using preprocessing singleton"""
    preprocessing = get_preprocessing()
    
    # Test JSON string conversion
    json_string = '{"title": "test title", "content": "test content"}'
    try:
        json_obj = preprocessing.string_to_json(json_string)
        print(f"JSON conversion successful: {json_obj}")
        return json_obj
    except Exception as e:
        print(f"JSON conversion failed: {e}")
        return None

# Method 3: Using in a service-like function
def process_document_text(text: str) -> str:
    """Process document text using the global preprocessing instance"""
    preprocessing = get_global_preprocessing()
    return preprocessing.text_preprocessing_vietnamese(text)

if __name__ == "__main__":
    print("=== PreProcessing Singleton Usage Examples ===")
    
    print("\n1. Using global instance:")
    example_using_global()
    
    print("\n2. Using singleton directly:")
    example_using_singleton()
    
    print("\n3. Using in a service function:")
    sample_text = "Xin chào! Đây là ví dụ về xử lý văn bản tiếng Việt."
    processed = process_document_text(sample_text)
    print(f"Service processed text: {processed}")