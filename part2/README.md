# HBnB Project

This project implements a simplified version of an Airbnb-like application. It includes classes for users, places, reviews, and amenities, each with specific attributes and methods to manage the application effectively.

## Overview

### BaseModel

The BaseModel class provides common attributes and methods for other classes in the application. It includes:

- **Attributes**:
  - id: Unique identifier for each instance.
  - created_at: Timestamp of when the instance was created.
  - updated_at: Timestamp of the last update.

- **Methods**:
  - save(): Updates the updated_at timestamp.
  - update(data): Updates attributes based on a provided dictionary.

### User

The User class inherits from BaseModel and represents a user in the system. Key features include:

- **Attributes**:
  - first_name: User's first name.
  - last_name: User's last name.
  - email: User's email address.
  - is_admin: Indicates if the user has admin privileges.

- **Methods**:
  - validate_fields(): Validates user attributes, ensuring email uniqueness and proper formatting.
  - delete_user(): Removes the user from the system.

### Review

The Review class inherits from BaseModel and represents a review for a place. It includes:

- **Attributes**:
  - text: Content of the review.
  - rating: Rating score (1-5).
  - place: The place being reviewed.
  - user: The user who wrote the review.

- **Methods**:
  - validate_fields(): Validates review attributes.
  - is_unique_review(user, place, reviews): Checks if the user has already reviewed the place.

### Amenity

The Amenity class inherits from BaseModel and represents an amenity associated with a place. Features include:

- **Attributes**:
  - name: Name of the amenity.

- **Methods**:
  - validate_fields(): Validates the amenity name for uniqueness and character constraints.
  - add_to_existing_names(): Adds the amenity name to a set of existing names if it is unique.

### Place

The Place class represents a place available for rent and inherits from BaseModel. Key attributes and methods include:

- **Attributes**:
  - title: Title of the place.
  - description: Optional description of the place.
  - price: Price per night.
  - latitude and longitude: Geographical coordinates.
  - owner: The user who owns the place.
  - reviews: List of reviews associated with the place.
  - amenities: List of amenities associated with the place.

- **Methods**:
  - validate_fields(): Validates the place attributes.
  - add_review(review): Adds a review to the place.
  - list_reviews(): Returns a list of all reviews for the place.
  - add_amenity(amenity): Adds an amenity to the place.
  - list_amenities(): Returns a list of all amenities for the place.

## Usage

Instantiate objects from the classes and use their methods to manage users, places, reviews, and amenities in the application.

### Example

```python

# Create a user

user = User(first_name="John", last_name="Doe", email="<john@example.com>")

# Create a place

place = Place(title="Cozy Cottage", price=100, latitude=35.0,
              longitude=-120.0, owner=user)

# Add a review

review = Review(text="Great place!", rating=5, place=place, user=user)
place.add_review(review)

# List reviews for the place

print(place.list_reviews())
