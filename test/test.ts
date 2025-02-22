type Item = {
    [key: string]: any; // Generic object type, key-value pairs can be anything
  };
  
  function sortByField(items: Item[], field: string): Item[] {
    return items.sort((a, b) => {
      // Check if the field exists in both objects
      const valueA = a[field];
      const valueB = b[field];
  
      if (valueA === undefined || valueB === undefined) {
        return 0; // If either value is missing, they are considered equal
      }
  
      // Check if the field is a date string and convert it to Date
      if (isDate(valueA) && isDate(valueB)) {
        const dateA = new Date(valueA);
        const dateB = new Date(valueB);
        return dateA.getTime() - dateB.getTime();
      }
  
      // If it's a number or can be converted to a number
      const numA = Number(valueA);
      const numB = Number(valueB);
      
      if (!isNaN(numA) && !isNaN(numB)) {
        return numA - numB;
      }
  
      // If it's a string, use lexicographical comparison
      return String(valueA).localeCompare(String(valueB));
    });
  }
  
  // Helper function to check if a value is a valid ISO date string
  function isDate(value: any): boolean {
    const date = Date.parse(value);
    return !isNaN(date);
  }
  
  // Example usage
  const items = [
    { id: "2025-02-22T00:00:00Z", name: "Banana" },
    { id: "2023-02-22T00:00:00Z", name: "Apple" },
    { id: "2024-02-22T00:00:00Z", name: "Cherry" },
    { id: "5", name: "Grapes" }
  ];
  
  // Sorting by 'id' (Date or String Convertible to Number)
  console.log(sortByField(items, "id"));
  
  // Sorting by 'name' (String)
  console.log(sortByField(items, "name"));
  