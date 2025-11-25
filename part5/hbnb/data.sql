-- ================================
-- INITIAL DATA INSERTS
-- ================================

-- Insert the administrator user
INSERT INTO user (
    id, first_name, last_name, email, password, is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$Q0w7WF9OBG.uT9XBeNPFdeVqIuP89YJ6iY3Y93YApzijr6iHvEi0S',
    TRUE
);

-- Insert amenities
INSERT INTO amenity (id, name) VALUES
('d5817700-0607-4f6b-bc9a-f66e51a0f098', 'WiFi'),
('99c5b52c-92b2-4c7c-b3c1-05c1c0ad0a90', 'Swimming Pool'),
('e75d3380-5e53-4cea-a929-9be9a6cd9bb5', 'Air Conditioning');

