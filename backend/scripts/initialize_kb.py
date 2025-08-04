#!/usr/bin/env python3
"""
Script to initialize the knowledge base with sample educational content.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.rag_service import rag_service
from langchain.schema import Document

def load_sample_content():
    """Load sample educational content from files"""
    sample_dir = Path(__file__).parent.parent / "data"
    documents = []
    
    # Load sample content file
    sample_file = sample_dir / "sample_content.txt"
    if sample_file.exists():
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": "sample_content.txt",
                    "description": "Introduction to Machine Learning",
                    "type": "educational_content"
                }
            ))
    
    # Add some additional educational content
    additional_content = [
        {
            "content": """
# Python Programming Fundamentals

Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in data science, web development, automation, and artificial intelligence.

## Key Features

1. **Readable Syntax**: Python's syntax is designed to be readable and straightforward
2. **Dynamic Typing**: Variables can change types during execution
3. **Automatic Memory Management**: Garbage collection handles memory allocation
4. **Large Standard Library**: Extensive built-in modules and packages
5. **Cross-platform**: Runs on Windows, macOS, and Linux

## Basic Data Types

- **Integers**: Whole numbers (1, 2, 3, -1, -2)
- **Floats**: Decimal numbers (3.14, -0.001, 2.0)
- **Strings**: Text data ("Hello", 'Python', \"\"\"Multi-line\"\"\")
- **Booleans**: True or False values
- **Lists**: Ordered, mutable collections [1, 2, 3, "hello"]
- **Tuples**: Ordered, immutable collections (1, 2, 3)
- **Dictionaries**: Key-value pairs {"name": "John", "age": 30}
- **Sets**: Unordered collections of unique elements {1, 2, 3}

## Control Structures

### If Statements
```python
if condition:
    # code block
elif another_condition:
    # code block
else:
    # code block
```

### Loops
```python
# For loop
for item in iterable:
    # code block

# While loop
while condition:
    # code block
```

## Functions

Functions are reusable blocks of code that perform specific tasks.

```python
def function_name(parameters):
    # function body
    return result
```

## Object-Oriented Programming

Python supports OOP with classes and objects:

```python
class MyClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"
```

## Best Practices

1. **Use meaningful variable names**
2. **Follow PEP 8 style guidelines**
3. **Write docstrings for functions and classes**
4. **Handle exceptions properly**
5. **Use virtual environments for projects**
6. **Write unit tests**
""",
            "metadata": {
                "source": "python_fundamentals",
                "description": "Python Programming Fundamentals",
                "type": "programming_tutorial"
            }
        },
        {
            "content": """
# Web Development with React

React is a JavaScript library for building user interfaces, particularly single-page applications. It's maintained by Facebook and a community of developers.

## Core Concepts

### Components
Components are the building blocks of React applications. They are reusable pieces of UI that can contain their own logic and styling.

```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}!</h1>;
}
```

### JSX
JSX is a syntax extension for JavaScript that allows you to write HTML-like code in your JavaScript files.

### Props
Props (properties) are used to pass data from parent components to child components.

### State
State is used to manage component-specific data that can change over time.

## Hooks

Hooks are functions that allow you to use state and other React features in functional components.

### useState
```jsx
import React, { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

### useEffect
```jsx
import React, { useState, useEffect } from 'react';

function DataFetcher() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetch('/api/data')
      .then(response => response.json())
      .then(data => setData(data));
  }, []);
  
  return <div>{data ? JSON.stringify(data) : 'Loading...'}</div>;
}
```

## Component Lifecycle

1. **Mounting**: Component is created and inserted into DOM
2. **Updating**: Component re-renders due to props or state changes
3. **Unmounting**: Component is removed from DOM

## Best Practices

1. **Keep components small and focused**
2. **Use functional components with hooks**
3. **Avoid prop drilling with Context API**
4. **Optimize performance with React.memo and useMemo**
5. **Write clean, readable JSX**
6. **Use TypeScript for better type safety**
""",
            "metadata": {
                "source": "react_tutorial",
                "description": "Web Development with React",
                "type": "web_development"
            }
        }
    ]
    
    for item in additional_content:
        documents.append(Document(
            page_content=item["content"],
            metadata=item["metadata"]
        ))
    
    return documents

def main():
    """Main function to initialize the knowledge base"""
    print("Initializing knowledge base with sample content...")
    
    try:
        # Load sample documents
        documents = load_sample_content()
        
        if not documents:
            print("No sample documents found!")
            return
        
        # Add documents to knowledge base
        success = rag_service.add_documents(documents)
        
        if success:
            print(f"Successfully added {len(documents)} documents to knowledge base")
            
            # Get knowledge base info
            info = rag_service.get_knowledge_base_info()
            print(f"Knowledge base now contains {info['total_documents']} documents")
            print(f"FAISS index size: {info['index_size']}")
        else:
            print("Failed to add documents to knowledge base")
            
    except Exception as e:
        print(f"Error initializing knowledge base: {e}")

if __name__ == "__main__":
    main() 