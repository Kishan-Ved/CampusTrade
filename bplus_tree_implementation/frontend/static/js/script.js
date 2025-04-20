// JavaScript for the B+ Tree Database UI

document.addEventListener('DOMContentLoaded', function() {
    // Example schema templates
    const schemaTemplates = {
        'memberExt': {
            'Member_ID': {'type': 'int', 'primary_key': true},
            'Name': {'type': 'string', 'nullable': false},
            'Email': {'type': 'string', 'nullable': false},
            'Password': {'type': 'string', 'nullable': false},
            'Contact_No': {'type': 'string', 'nullable': false},
            'Age': {'type': 'int', 'nullable': false},
            'Profile_Image': {'type': 'blob', 'nullable': true},
            'Role': {'type': 'string', 'nullable': false},
            'Registered_On': {'type': 'timestamp', 'nullable': true}
        },
        'category': {
            'Category_ID': {'type': 'int', 'primary_key': true},
            'Category_Name': {'type': 'string', 'nullable': false}
        },
        'product_listing': {
            'Product_ID': {'type': 'int', 'primary_key': true},
            'Seller_ID': {'type': 'int', 'nullable': false},
            'Title': {'type': 'string', 'nullable': false},
            'Description': {'type': 'string', 'nullable': false},
            'Price': {'type': 'float', 'nullable': false},
            'Category_ID': {'type': 'int', 'nullable': false},
            'Condition_': {'type': 'string', 'nullable': false},
            'Image_URL': {'type': 'string', 'nullable': true},
            'Listed_On': {'type': 'timestamp', 'nullable': true}
        }
    };
    
    // Add template buttons to the schema textarea
    const schemaTextarea = document.getElementById('table-schema');
    if (schemaTextarea) {
        const templateContainer = document.createElement('div');
        templateContainer.className = 'mt-2';
        templateContainer.innerHTML = '<small class="form-text text-muted">Use template: </small>';
        
        for (const template in schemaTemplates) {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'btn btn-sm btn-outline-secondary ms-1';
            button.textContent = template;
            button.addEventListener('click', function() {
                schemaTextarea.value = JSON.stringify(schemaTemplates[template], null, 2);
            });
            templateContainer.appendChild(button);
        }
        
        schemaTextarea.parentNode.insertBefore(templateContainer, schemaTextarea.nextSibling);
    }
    
    // Add example data for insert row
    const insertRowTextarea = document.getElementById('insert-row');
    if (insertRowTextarea) {
        const tableName = document.querySelector('h1').textContent.trim();
        let exampleData = {};
        
        if (tableName === 'memberExt') {
            exampleData = {
                'Member_ID': 16,
                'Name': 'John Doe',
                'Email': 'john@example.com',
                'Password': 'hashedpassword',
                'Contact_No': '9876543225',
                'Age': 25,
                'Role': 'Student'
            };
        } else if (tableName === 'category') {
            exampleData = {
                'Category_ID': 15,
                'Category_Name': 'Computer Accessories'
            };
        } else if (tableName === 'product_listing') {
            exampleData = {
                'Product_ID': 14,
                'Seller_ID': 1,
                'Title': 'Gaming Mouse',
                'Description': 'High-precision gaming mouse with RGB lighting',
                'Price': 45.99,
                'Category_ID': 1,
                'Condition_': 'New'
            };
        }
        
        const exampleButton = document.createElement('button');
        exampleButton.type = 'button';
        exampleButton.className = 'btn btn-sm btn-outline-secondary mt-2';
        exampleButton.textContent = 'Load Example';
        exampleButton.addEventListener('click', function() {
            insertRowTextarea.value = JSON.stringify(exampleData, null, 2);
        });
        
        insertRowTextarea.parentNode.insertBefore(exampleButton, insertRowTextarea.nextSibling);
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 1s';
            setTimeout(function() {
                alert.remove();
            }, 1000);
        }, 5000);
    });
    
    // Confirm before dangerous operations
    const dangerousForms = document.querySelectorAll('form button.btn-danger');
    dangerousForms.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to perform this operation?')) {
                event.preventDefault();
            }
        });
    });
});
