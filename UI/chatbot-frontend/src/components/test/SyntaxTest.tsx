import React, { useState } from 'react';
import CodeBlock from '../chat/CodeBlock';

const SyntaxTest: React.FC = () => {
  const [copiedBlocks, setCopiedBlocks] = useState<{ [key: number]: boolean }>({});

  const handleCopy = (code: string, blockIndex: number) => {
    navigator.clipboard.writeText(code);
    setCopiedBlocks(prev => ({ ...prev, [blockIndex]: true }));
    setTimeout(() => {
      setCopiedBlocks(prev => ({ ...prev, [blockIndex]: false }));
    }, 2000);
  };

  const testCodes = [
    {
      language: 'javascript',
      code: `function greet(name) {
  const message = \`Hello, \${name}!\`;
  console.log(message);
  return message;
}

// Call the function
const result = greet("World");`
    },
    {
      language: 'typescript',
      code: `interface User {
  id: number;
  name: string;
  email?: string;
}

class UserService {
  private users: User[] = [];

  addUser(user: User): void {
    this.users.push(user);
  }

  getUserById(id: number): User | undefined {
    return this.users.find(user => user.id === id);
  }
}`
    },
    {
      language: 'python',
      code: `def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    
    return b

# Example usage
result = calculate_fibonacci(10)
print(f"The 10th Fibonacci number is: {result}")`
    },
    {
      language: 'css',
      code: `.container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.button:hover {
  transform: translateY(-2px);
  transition: all 0.3s ease;
}`
    }
  ];

  return (
    <div className="p-6 space-y-6 bg-white dark:bg-gray-900 min-h-screen">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Syntax Highlighting Test
      </h1>
      
      {testCodes.map((test, index) => (
        <div key={index}>
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
            {test.language.charAt(0).toUpperCase() + test.language.slice(1)} Example
          </h2>
          <CodeBlock
            code={test.code}
            language={test.language}
            blockIndex={index}
            copied={copiedBlocks[index] || false}
            onCopy={handleCopy}
          />
        </div>
      ))}
    </div>
  );
};

export default SyntaxTest;
