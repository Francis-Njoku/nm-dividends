# Nairametrics Dividends API Documentation

**Base URL:** `http://localhost:8000` (dev) / Your production URL

**Authentication:** JWT Bearer Token

**API Documentation:** Interactive Swagger UI available at `/` when the backend is running.

---

## Table of Contents

1. [Authentication](#authentication)
2. [Token Management](#token-management)
3. [User Management](#user-management)
4. [Email Verification](#email-verification)
5. [Password Reset](#password-reset)
6. [Referral System](#referral-system)
7. [Investments](#investments)
8. [Investor Operations](#investor-operations)
9. [Articles/Blog](#articlesblog)
10. [Comments](#comments)
11. [Income & Expenses](#income--expenses)
12. [Results/CSV Data](#resultscsv-data)
13. [Error Responses](#error-responses)
14. [Data Models](#data-models)

---

## Authentication

### 1. Login

**Endpoint:** `POST /auth/login/`

**Description:** Authenticate a user and receive JWT tokens.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Success Response (200 OK):**

```json
{
  "email": "user@example.com",
  "username": "john123",
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "is_staff": false,
  "is_approved": true
}
```

**Error Responses:**

- `401 Unauthorized`: Invalid credentials
- `401 Unauthorized`: Email is not verified
- `401 Unauthorized`: Account disabled, contact admin

---

### 2. Register

**Endpoint:** `POST /auth/register/`

**Description:** Register a new user account. User will receive an email verification link.

**Request Body:**

```json
{
  "firstname": "John",
  "lastname": "Doe",
  "email": "user@example.com",
  "password": "SecurePassword123",
  "callBackUrl": "http://localhost:3000/confirm_email"
}
```

**Success Response (201 Created):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "JohnDoe12345",
  "firstname": "John",
  "lastname": "Doe",
  "referral_code": "ABC123XYZ"
}
```

**Notes:**

- `username` is auto-generated from `firstname` + `lastname` + random number
- `referral_code` is auto-generated
- Email verification link is sent to the user's email
- User is automatically approved (`is_approved: true`)

**Error Responses:**

- `400 Bad Request`: Validation errors (email exists, weak password, etc.)

---

### 3. Logout

**Endpoint:** `POST /auth/logout/`

**Authentication:** Required (Bearer Token)

**Description:** Logout user and blacklist the refresh token.

**Request Body:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response (204 No Content):** Empty body

**Error Responses:**

- `401 Unauthorized`: Token is expired or invalid

---

### 4. Load Current User

**Endpoint:** `GET /auth/loaduser/`

**Authentication:** Required (Bearer Token)

**Description:** Get the current authenticated user's details.

**Success Response (200 OK):**

```json
{
  "user": {
    "id": 1,
    "username": "john123",
    "email": "user@example.com",
    "firstname": "John",
    "lastname": "Doe",
    "is_verified": true,
    "is_approved": true,
    "is_staff": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:45:00Z"
  }
}
```

---

## Token Management

### Refresh Access Token

**Endpoint:** `POST /auth/refresh/`

**Description:** Get a new access token using a refresh token.

**Request Body:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response (200 OK):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error Responses:**

- `401 Unauthorized`: Token is invalid or expired
- `401 Unauthorized`: Token is blacklisted

**Note:** Access tokens typically expire after 30 minutes. Implement automatic token refresh in your frontend.

---

## User Management

### 1. Get User by ID

**Endpoint:** `GET /auth/user/<id>/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
{
  "id": 1,
  "firstname": "John",
  "lastname": "Doe",
  "email": "user@example.com",
  "address": "123 Main St",
  "phone": "+1234567890",
  "referral_code": "ABC123XYZ",
  "is_verified": true,
  "is_approved": true,
  "created_at": "2024-01-15T10:30:00Z",
  "details": []
}
```

---

### 2. List All Users (Admin Only)

**Endpoint:** `GET /auth/list-users/`

**Authentication:** Required (Bearer Token + Admin)

**Query Parameters:**

- `firstname` - Filter by first name
- `lastname` - Filter by last name
- `phone` - Filter by phone
- `email` - Filter by email
- `referral_code` - Filter by referral code
- `search` - Search across multiple fields
- `ordering` - Order results (e.g., `created_at`, `-created_at`)

**Success Response (200 OK):**

```json
{
  "count": 100,
  "next": "http://localhost:8000/auth/list-users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "firstname": "John",
      "lastname": "Doe",
      "email": "user@example.com",
      "address": "123 Main St",
      "phone": "+1234567890",
      "referral_code": "ABC123XYZ",
      "is_verified": true,
      "is_approved": true,
      "created_at": "2024-01-15T10:30:00Z",
      "details": []
    }
  ]
}
```

---

### 3. Approve User (Admin Only)

**Endpoint:** `PATCH /auth/approve/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "is_approved": true
}
```

**Success Response (200 OK):**

```json
{
  "id": 1,
  "is_approved": true
}
```

---

### 4. Verify User (Admin Only)

**Endpoint:** `PATCH /auth/verify/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "is_verified": true
}
```

**Success Response (200 OK):**

```json
{
  "id": 1,
  "is_verified": true
}
```

---

### 5. Export Users to CSV (Admin Only)

**Endpoint:** `GET /auth/export/users/`

**Authentication:** Required (Bearer Token + Admin)

**Response:** CSV file download

---

### 6. Export Users to PDF (Admin Only)

**Endpoint:** `GET /auth/export/users/pdf/`

**Authentication:** Required (Bearer Token + Admin)

**Response:** PDF file download

---

## Email Verification

### Verify Email

**Endpoint:** `GET /auth/email-verify/?token=<jwt_token>`

**Description:** Verify user's email address using the token sent via email.

**Query Parameters:**

- `token` - JWT token from the verification email

**Success Response (200 OK):**

```json
{
  "email": "Successfully activated"
}
```

**Error Responses:**

- `400 Bad Request`: Activation Expired
- `400 Bad Request`: Invalid token

---

## Password Reset

### 1. Request Password Reset Email

**Endpoint:** `POST /auth/request-reset-email/`

**Description:** Send a password reset email to the user.

**Request Body:**

```json
{
  "email": "user@example.com",
  "callbackUrl": "http://localhost:3000",
  "redirect_url": "http://localhost:3000/reset-password"
}
```

**Success Response (200 OK):**

```json
{
  "success": "We have sent you a link to reset your password"
}
```

---

### 2. Check Password Reset Token

**Endpoint:** `GET /auth/password-reset/<uidb64>/<token>/?redirect_url=<url>`

**Description:** Validate the password reset token and redirect to the frontend.

**Success Response:** Redirects to `redirect_url?token_valid=True&message=Credentials Valid&uidb64=<uidb64>&token=<token>`

**Error Response:** Redirects to `redirect_url?token_valid=False`

---

### 3. Set New Password

**Endpoint:** `PATCH /auth/password-reset-complete`

**Description:** Complete the password reset process.

**Request Body:**

```json
{
  "password": "NewSecurePassword123",
  "token": "<token_from_redirect>",
  "uidb64": "<uidb64_from_redirect>"
}
```

**Success Response (200 OK):**

```json
{
  "success": true,
  "message": "Password reset success"
}
```

**Error Responses:**

- `401 Unauthorized`: The reset link is invalid

---

## Referral System

### Get User by Referral Code

**Endpoint:** `GET /auth/invite/?user=<referral_code>`

**Description:** Get user details by their referral code.

**Query Parameters:**

- `user` - Referral code

**Success Response (200 OK):**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "referral_code": "ABC123XYZ"
  }
}
```

**Error Responses:**

- `400 Bad Request`: Object with referral code does not exist

---

## Investments

### 1. List All Investments

**Endpoint:** `GET /investment/investment/`

**Authentication:** Required (Bearer Token)

**Query Parameters:**

- `name` - Filter by investment name
- `location` - Filter by location
- `search` - Search across name and location
- `ordering` - Order results (e.g., `created_at`, `-created_at`)

**Success Response (200 OK):**

```json
[
  {
    "id": 1,
    "name": "Luxury Apartments",
    "description": "Premium residential apartments...",
    "location": "Lagos, Nigeria",
    "amount": 50000000,
    "roi": 15.5,
    "currency": 1,
    "dealtype": 1,
    "room": 1,
    "period": 1,
    "risk": 1,
    "volume": 100,
    "is_verified": true,
    "is_closed": false,
    "start_date": "2024-01-01",
    "end_date": "2025-12-31",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 2. Get Investment by Slug

**Endpoint:** `GET /investment/portfolio/<slug>/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
{
  "id": 1,
  "name": "Luxury Apartments",
  "slug": "luxury-apartments-abc123",
  "description": "Premium residential apartments...",
  "location": "Lagos, Nigeria",
  "amount": 50000000,
  "project_cost": 45000000,
  "project_raise": 50000000,
  "roi": 15.5,
  "annualized": 12.3,
  "currency": {
    "id": 1,
    "name": "NGN"
  },
  "dealtype": {
    "id": 1,
    "name": "Real Estate"
  },
  "room": {
    "id": 1,
    "name": "Residential",
    "slug": "residential"
  },
  "period": {
    "id": 1,
    "period": "12 months"
  },
  "risk": {
    "id": 1,
    "risk": "Low"
  },
  "volume": 100,
  "only_returns": true,
  "off_plan": false,
  "outright_purchase": true,
  "offer_price": 52000000,
  "spot_price": 51000000,
  "unit_price": 500000,
  "is_verified": true,
  "is_closed": false,
  "title_status": "approved",
  "construction_status": "in progress",
  "project_status": "started",
  "start_date": "2024-01-01",
  "end_date": "2025-12-31",
  "offer_period": "2024-12-31",
  "milestone": 3,
  "minimum_allotment": 1000000,
  "maximum_allotment": 10000000,
  "features": "Swimming pool, gym, 24/7 security",
  "video": "https://youtube.com/watch?v=example",
  "gallery_set": [
    {
      "id": 1,
      "gallery": "http://localhost:8000/media/posts/image1.jpg",
      "is_featured": true
    }
  ],
  "owner": {
    "id": 1,
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:45:00Z"
}
```

---

### 3. List Investments by Room Category

**Endpoint:** `GET /investment/investment/room/<slug>/`

**Authentication:** Required (Bearer Token)

**Description:** Get all investments in a specific room category.

**Success Response (200 OK):** Array of investment objects (same structure as above)

---

### 4. List Issuer's Investments

**Endpoint:** `GET /investment/investment/issuer/`

**Authentication:** Required (Bearer Token)

**Description:** Get all investments created by the authenticated user (issuer).

**Success Response (200 OK):** Array of investment objects (same structure as above)

---

### 5. Create Investment (Admin Only)

**Endpoint:** `POST /investment/invest/`

**Authentication:** Required (Bearer Token + Admin)

**Content-Type:** `multipart/form-data`

**Request Body:**

```json
{
  "name": "Luxury Apartments",
  "description": "Premium residential apartments...",
  "location": "Lagos, Nigeria",
  "volume": 100,
  "video": "https://youtube.com/watch?v=example",
  "title_status": "approved",
  "construction_status": "in progress",
  "project_status": "started",
  "features": "Swimming pool, gym, 24/7 security",
  "start_date": "2024-01-01",
  "end_date": "2025-12-31",
  "gallery": "Image file",
  "galleries_1": "Additional image file",
  "galleries_2": "Additional image file",
  "galleries_3": "Additional image file",
  "galleries_4": "Additional image file",
  "investors": "CSV file with investor data"
}
```

**Success Response (201 Created):** Investment object

**Notes:**

- `gallery` is set as featured image
- `galleries_1-4` are additional images
- `investors` CSV file can create new users and add them as investors
- CSV format: `firstname, lastname, email, address, phone, dob, nin, next_of_kin, unit_number, amount, payment`

---

### 6. Update Investment (Admin Only)

**Endpoint:** `PUT /investment/invest/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Content-Type:** `multipart/form-data`

**Request Body:** Same as create investment

**Success Response (200 OK):** Updated investment object

---

### 7. Delete Investment (Admin Only)

**Endpoint:** `DELETE /investment/invest/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (204 No Content):** Empty body

---

### 8. Approve Investment (Admin Only)

**Endpoint:** `PATCH /investment/approve/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "is_verified": true
}
```

**Success Response (200 OK):**

```json
{
  "id": 1,
  "is_verified": true
}
```

---

### 9. Close Investment

**Endpoint:** `PATCH /investment/close/<id>/`

**Authentication:** Required (Bearer Token)

**Request Body:**

```json
{
  "is_closed": true
}
```

**Success Response (200 OK):**

```json
{
  "id": 1,
  "is_closed": true
}
```

---

### 10. Investment Summary (Issuer)

**Endpoint:** `GET /investment/issuer/summary/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
{
  "totalInvestors": 50,
  "totalInvestments": 5,
  "totalSponsors": 3,
  "totalVolume": 500,
  "totalInvestorVolume": { "volume": 250 }
}
```

---

### 11. Investment Summary (Investor)

**Endpoint:** `GET /investment/investor/summary/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
{
  "totalInvestments": 10,
  "totalVolume": 50
}
```

---

### 12. Investment Summary (Admin)

**Endpoint:** `GET /investment/admin/summary/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):**

```json
{
  "totalInvestors": 500,
  "totalInvestments": 50,
  "totalSponsors": 30,
  "totalVolume": 5000,
  "totalInvestorVolume": { "volume": 2500 }
}
```

---

### 13. Add Gallery Image (Admin Only)

**Endpoint:** `POST /investment/image/`

**Authentication:** Required (Bearer Token + Admin)

**Content-Type:** `multipart/form-data`

**Request Body:**

```json
{
  "investment": 1,
  "gallery": "Image file"
}
```

**Success Response (201 Created):** Gallery object

---

### 14. Update Gallery Image (Admin Only)

**Endpoint:** `PATCH /investment/image/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "is_featured": true
}
```

**Success Response (200 OK):** Updated gallery object

---

### 15. Delete Gallery Image (Admin Only)

**Endpoint:** `DELETE /investment/image/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (204 No Content):** Empty body

---

### 16. Create Sponsor

**Endpoint:** `POST /investment/create/sponsor/<id>/`

**Authentication:** Required (Bearer Token)

**Content-Type:** `multipart/form-data`

**Request Body:**

```json
{
  "nin": "12345678901",
  "name": "Jane Smith",
  "dob": "1980-01-01",
  "address": "123 Main St",
  "identity": "ID card file",
  "phone": "+1234567890"
}
```

**Success Response (201 Created):** Sponsor investment object

**Notes:**

- If sponsor with NIN exists, it will be linked
- If not, a new sponsor will be created

---

### 17. Update Sponsor (Admin Only)

**Endpoint:** `PATCH /investment/update/sponsor/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "name": "Updated Name",
  "is_verified": true
}
```

**Success Response (200 OK):** Updated sponsor object

---

### 18. Approve Sponsor (Admin Only)

**Endpoint:** `PATCH /investment/verify/sponsor/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "is_verified": true
}
```

**Success Response (200 OK):** Updated sponsor object

---

### 19. List Sponsors (Admin Only)

**Endpoint:** `GET /investment/sponsors/`

**Authentication:** Required (Bearer Token + Admin)

**Query Parameters:**

- `name` - Filter by name
- `nin` - Filter by NIN
- `phone` - Filter by phone
- `search` - Search across fields

**Success Response (200 OK):** Array of sponsor objects

---

### 20. List Sponsor's Investments

**Endpoint:** `GET /investment/sponsor/<id>/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):** Array of investment objects

---

### 21. List Investment Rooms (Admin Only)

**Endpoint:** `GET /investment/room/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Array of room objects

---

### 22. List All Investment Rooms

**Endpoint:** `GET /investment/room/all/`

**Authentication:** Not Required

**Success Response (200 OK):** Array of room objects

---

### 23. List Main Rooms (Admin Only)

**Endpoint:** `GET /investment/mainroom/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Array of main room objects

---

### 24. List All Main Rooms

**Endpoint:** `GET /investment/mainroom/all/`

**Authentication:** Not Required

**Success Response (200 OK):** Array of main room objects

---

### 25. List Currencies

**Endpoint:** `GET /investment/currency/`

**Authentication:** Not Required

**Success Response (200 OK):** Array of currency objects

---

### 26. Create Currency (Admin Only)

**Endpoint:** `POST /investment/currency/create/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "name": "USD",
  "is_active": true
}
```

**Success Response (201 Created):** Currency object

---

### 27. Update Currency (Admin Only)

**Endpoint:** `PUT /investment/currency/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Updated currency object

---

### 28. Delete Currency (Admin Only)

**Endpoint:** `DELETE /investment/currency/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (204 No Content):** Empty body

---

### 29. List Deal Types

**Endpoint:** `GET /investment/dealtype/`

**Authentication:** Not Required

**Success Response (200 OK):** Array of deal type objects

---

### 30. Create Deal Type (Admin Only)

**Endpoint:** `POST /investment/dealtype/create/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "name": "Real Estate",
  "is_active": true
}
```

**Success Response (201 Created):** Deal type object

---

### 31. Update Deal Type (Admin Only)

**Endpoint:** `PUT /investment/dealtype/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Updated deal type object

---

### 32. Delete Deal Type (Admin Only)

**Endpoint:** `DELETE /investment/dealtype/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (204 No Content):** Empty body

---

### 33. Get Investor Returns

**Endpoint:** `GET /investment/investor/returns/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
{
  "NGN": 5750000,
  "USD": 12000,
  "GBP": 9500,
  "EURO": 11000
}
```

**Note:** Returns total returns (principal + ROI) by currency for approved investments

---

### 34. Get Investor Subscriptions Count

**Endpoint:** `GET /investment/investor/subscriptions/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
{
  "investments": 5
}
```

---

### 35. Get Investor Pending Subscriptions Count

**Endpoint:** `GET /investment/investor/subscriptions/n/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
{
  "pendingInvestments": 2
}
```

---

### 36. Get Total Amount Invested

**Endpoint:** `GET /investment/investor/amounts/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
{
  "NGN": 5000000,
  "USD": 10000,
  "GBP": 8000,
  "EURO": 9500
}
```

---

### 37. Admin Export Investments

**Endpoint:** `GET /investment/admin/export/`

**Authentication:** Required (Bearer Token + Admin)

**Response:** CSV file download

---

### 38. Add Investor to Investment (Issuer)

**Endpoint:** `POST /investment/issuer/investor/<id>/`

**Authentication:** Required (Bearer Token)

**Request Body:**

```json
{
  "firstname": "Jane",
  "lastname": "Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "address": "123 Main St",
  "dob": "1980-01-01",
  "nin": "12345678901",
  "next_of_kin": "John Smith",
  "house_number": "A101",
  "amount": 1000000,
  "payment": "full",
  "volume": 1
}
```

**Success Response (201 Created):** Investor object

**Notes:**

- If user doesn't exist, a new account will be created
- Default password: `firstname + lastname + random_string`
- Email with credentials will be sent to the user

---

### 39. Remove Investor from Investment (Issuer)

**Endpoint:** `POST /investment/remove/investor/<id>/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
{
  "success": "Investor has been removed"
}
```

---

### 40. Remove Investor from Investment (Admin)

**Endpoint:** `POST /investment/admin/remove/investor/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):**

```json
{
  "success": "Investor has been removed"
}
```

---

## Investor Operations

### 1. List Periods (Admin Only)

**Endpoint:** `GET /investor/period/`

**Authentication:** Required (Bearer Token + Admin)

**Query Parameters:**

- `period` - Filter by period
- `is_verified` - Filter by verification status
- `search` - Search across period field
- `ordering` - Order results

**Success Response (200 OK):** Array of period objects

---

### 2. Create Period (Admin Only)

**Endpoint:** `POST /investor/period/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "period": "12 months",
  "is_verified": true
}
```

**Success Response (201 Created):** Period object

---

### 3. Update Period (Admin Only)

**Endpoint:** `PUT /investor/period/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Updated period object

---

### 4. Delete Period (Admin Only)

**Endpoint:** `DELETE /investor/period/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (204 No Content):** Empty body

---

### 5. List All Periods

**Endpoint:** `GET /investor/period/all/`

**Authentication:** Not Required

**Success Response (200 OK):** Array of period objects

---

### 6. List Risks (Admin Only)

**Endpoint:** `GET /investor/risk/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Array of risk objects

---

### 7. Create Risk (Admin Only)

**Endpoint:** `POST /investor/risk/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "risk": "Low",
  "is_verified": true
}
```

**Success Response (201 Created):** Risk object

---

### 8. Update Risk (Admin Only)

**Endpoint:** `PUT /investor/risk/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Updated risk object

---

### 9. Delete Risk (Admin Only)

**Endpoint:** `DELETE /investor/risk/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (204 No Content):** Empty body

---

### 10. List All Risks

**Endpoint:** `GET /investor/risk/all/`

**Authentication:** Not Required

**Success Response (200 OK):** Array of risk objects

---

### 11. List Investment Sizes (Admin Only)

**Endpoint:** `GET /investor/size/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Array of size objects

---

### 12. Create Investment Size (Admin Only)

**Endpoint:** `POST /investor/size/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "investment_size": "Large",
  "is_verified": true
}
```

**Success Response (201 Created):** Size object

---

### 13. Update Investment Size (Admin Only)

**Endpoint:** `PUT /investor/size/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Updated size object

---

### 14. Delete Investment Size (Admin Only)

**Endpoint:** `DELETE /investor/size/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (204 No Content):** Empty body

---

### 15. List All Investment Sizes

**Endpoint:** `GET /investor/size/all/`

**Authentication:** Not Required

**Success Response (200 OK):** Array of size objects

---

### 16. List Interests (Admin Only)

**Endpoint:** `GET /investor/interest/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Array of interest objects

---

### 17. Create Interest (Admin Only)

**Endpoint:** `POST /investor/interest/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "interest": "High Returns",
  "is_verified": true
}
```

**Success Response (201 Created):** Interest object

---

### 18. Update Interest (Admin Only)

**Endpoint:** `PUT /investor/interest/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Updated interest object

---

### 19. Delete Interest (Admin Only)

**Endpoint:** `DELETE /investor/interest/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (204 No Content):** Empty body

---

### 20. List All Interests

**Endpoint:** `GET /investor/interest/all/`

**Authentication:** Not Required

**Success Response (200 OK):** Array of interest objects

---

### 21. Subscribe to Investment (Investor)

**Endpoint:** `POST /investor/investment/<id>/`

**Authentication:** Required (Bearer Token + User Approved)

**Request Body:**

```json
{
  "amount": 1000000,
  "bid_price": 1050000,
  "volume": 1,
  "investment_type": "only returns"
}
```

**Success Response (201 Created):** Investor object

**Notes:**

- User must be approved to subscribe
- Amount cannot exceed investment amount
- Investment types: `only returns`, `off plan`, `outright purchase`

---

### 22. Add Installment (Investor)

**Endpoint:** `POST /investor/installment/<id>/`

**Authentication:** Required (Bearer Token + User Approved)

**Request Body:**

```json
{
  "amount": 500000
}
```

**Success Response (201 Created):** Installment object

**Notes:**

- Total amount + installments cannot exceed bid price

---

### 23. List Investor's Subscriptions

**Endpoint:** `GET /investor/list/investment/`

**Authentication:** Required (Bearer Token + User Approved)

**Query Parameters:**

- `investment__name` - Filter by investment name
- `investment__location` - Filter by location
- `search` - Search across fields

**Success Response (200 OK):** Array of investor subscription objects

---

### 24. Get Investor Subscription Details

**Endpoint:** `GET /investor/list/investment/<id>/`

**Authentication:** Required (Bearer Token + User Approved)

**Success Response (200 OK):** Investor subscription object

---

### 25. Get Total Amount Invested

**Endpoint:** `GET /investor/total/amount/`

**Authentication:** Required (Bearer Token + User Approved)

**Success Response (200 OK):**

```json
{
  "amount": 5000000
}
```

---

### 26. Get Total Investments Count

**Endpoint:** `GET /investor/total/investments/`

**Authentication:** Required (Bearer Token + User Approved)

**Success Response (200 OK):**

```json
{
  "investments": 5
}
```

---

### 27. Get Total Investment Rooms Count

**Endpoint:** `GET /investor/total/rooms/`

**Authentication:** Required (Bearer Token + User Approved)

**Success Response (200 OK):** Number of unique investment rooms

---

### 28. Approve Investor Subscription (Admin Only)

**Endpoint:** `PATCH /investor/approve/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "is_approved": true
}
```

**Success Response (200 OK):** Updated investor object

**Note:** Also approves associated installment

---

### 29. Approve Installment (Admin Only)

**Endpoint:** `PATCH /investor/approve/installment/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "is_approved": true,
  "amount": 500000
}
```

**Success Response (200 OK):** Updated investor object with added amount

---

### 30. Close Investor Subscription (Admin Only)

**Endpoint:** `PATCH /investor/close/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "is_closed": true
}
```

**Success Response (200 OK):** Updated investor object

---

### 31. Update Investor Subscription

**Endpoint:** `PUT /investor/update/<id>/`

**Authentication:** Required (Bearer Token)

**Request Body:**

```json
{
  "amount": 1000000,
  "house_number": "A101",
  "payment": "full"
}
```

**Success Response (200 OK):** Updated investor object

---

### 32. Delete Investor Subscription

**Endpoint:** `DELETE /investor/update/<id>/`

**Authentication:** Required (Bearer Token)

**Success Response (204 No Content):** Empty body

---

### 33. Create Investment Subscription (Admin Only)

**Endpoint:** `POST /investor/admin/create/investment/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "investor": 5,
  "amount": 1000000,
  "bid_price": 1050000,
  "volume": 1,
  "investment_type": "only returns"
}
```

**Success Response (201 Created):** Investor object

---

### 34. Update Investor Subscription (Admin Only)

**Endpoint:** `PUT /investor/admin/update/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "amount": 1000000,
  "bid_price": 1050000,
  "investment": 1,
  "investor": 5,
  "is_approved": true,
  "is_closed": false
}
```

**Success Response (200 OK):** Updated investor object

---

### 35. Delete Investor Subscription (Admin Only)

**Endpoint:** `DELETE /investor/admin/update/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (204 No Content):** Empty body

---

### 36. List All Investor Subscriptions (Admin Only)

**Endpoint:** `GET /investor/admin/list/investment/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Array of all investor subscription objects

---

### 37. List All Users with Subscriptions (Admin Only)

**Endpoint:** `GET /investor/admin/list/investors/`

**Authentication:** Required (Bearer Token + Admin)

**Query Parameters:**

- `firstname` - Filter by first name
- `lastname` - Filter by last name
- `email` - Filter by email
- `phone` - Filter by phone
- `search` - Search across fields

**Success Response (200 OK):** Array of user objects with subscription details

---

### 38. Get User's Subscriptions (Admin Only)

**Endpoint:** `GET /investor/admin/investors/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Array of user objects

---

### 39. Get Single User's Subscriptions (Admin Only)

**Endpoint:** `GET /investor/admin/investor/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Array of investor subscription objects for specific user

---

### 40. List All Installments (Admin Only)

**Endpoint:** `GET /investor/admin/payments/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Array of installment objects

---

### 41. Admin Export Investors

**Endpoint:** `GET /investor/admin/export/`

**Authentication:** Required (Bearer Token + Admin)

**Response:** CSV file download

---

### 42. Contact Investment Issuer

**Endpoint:** `POST /investor/message/<id>/`

**Authentication:** Required (Bearer Token)

**Request Body:**

```json
{
  "message": "I'm interested in this investment..."
}
```

**Success Response (200 OK):** Empty body

---

## Articles/Blog

### 1. List All Articles

**Endpoint:** `GET /article/posts/`

**Authentication:** Not Required

**Success Response (200 OK):**

```json
[
  {
    "id": 1,
    "title": "Investment Guide 2024",
    "slug": "investment-guide-2024",
    "content": "<p>Detailed article content...</p>",
    "author": {
      "id": 1,
      "username": "john123",
      "email": "john@example.com"
    },
    "featured_image": "http://localhost:8000/media/featured_images/image.jpg",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:45:00Z"
  }
]
```

---

### 2. Create Article

**Endpoint:** `POST /article/posts/create/`

**Authentication:** Required (Bearer Token)

**Content-Type:** `multipart/form-data`

**Request Body:**

```json
{
  "title": "Investment Guide 2024",
  "content": "<p>Detailed article content...</p>",
  "featured_image": "Image file"
}
```

**Success Response (201 Created):** Article object

**Notes:**

- Slug is auto-generated from title
- Author is automatically set to authenticated user

---

### 3. Get Article by Slug

**Endpoint:** `GET /article/posts/<slug>/`

**Authentication:** Not Required

**Success Response (200 OK):** Article object (same structure as above)

---

### 4. Update Article

**Endpoint:** `PUT /article/posts/<slug>/update/`

**Authentication:** Required (Bearer Token)

**Content-Type:** `multipart/form-data`

**Request Body:** Same as create article

**Success Response (200 OK):** Updated article object

**Error Responses:**

- `403 Forbidden`: User is not the author

---

### 5. Delete Article

**Endpoint:** `DELETE /article/posts/<slug>/delete/`

**Authentication:** Required (Bearer Token)

**Success Response (204 No Content):** Empty body

**Error Responses:**

- `403 Forbidden`: User is not the author

---

## Comments

### 1. Create Comment on Investor Subscription

**Endpoint:** `POST /comment/create/<id>/`

**Authentication:** Required (Bearer Token)

**Request Body:**

```json
{
  "comment": "I have a question about this investment..."
}
```

**Success Response (201 Created):** Comment object

**Notes:**

- User must be subscribed to the investment
- Comment is linked to investor subscription

---

### 2. Create Comment on Investment

**Endpoint:** `POST /comment/create/investment/<id>/`

**Authentication:** Required (Bearer Token)

**Request Body:**

```json
{
  "comment": "I'm interested in this investment..."
}
```

**Success Response (201 Created):** Comment object

**Notes:**

- User must be subscribed to the investment
- Comment is linked to investment

---

### 3. Create Comment as Issuer

**Endpoint:** `POST /comment/issuer/create/investment/<id>/`

**Authentication:** Required (Bearer Token)

**Request Body:**

```json
{
  "comment": "Thank you for your interest..."
}
```

**Success Response (201 Created):** Comment object

**Notes:**

- Only investment owner can comment
- Comment is linked to investment

---

### 4. Create Comment as Admin

**Endpoint:** `POST /comment/admin/create/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Request Body:**

```json
{
  "comment": "Admin response...",
  "is_closed": false
}
```

**Success Response (201 Created):** Comment object

---

### 5. Get Investor Comments (Admin Only)

**Endpoint:** `GET /comment/investor/<id>/`

**Authentication:** Required (Bearer Token + Admin)

**Success Response (200 OK):** Investor object with comments

---

### 6. List All Comments (Admin Only)

**Endpoint:** `GET /comment/admin/list/`

**Authentication:** Required (Bearer Token + Admin)

**Query Parameters:**

- `serialkey` - Filter by serial key
- `search` - Search across fields

**Success Response (200 OK):** Array of investor objects with comments

---

## Income & Expenses

### 1. List Income

**Endpoint:** `GET /income/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
[
  {
    "id": 1,
    "source": "SALARY",
    "amount": "500000.00",
    "description": "Monthly salary",
    "date": "2024-01-15",
    "owner": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

**Note:** Only returns income for authenticated user

---

### 2. Create Income

**Endpoint:** `POST /income/`

**Authentication:** Required (Bearer Token)

**Request Body:**

```json
{
  "source": "SALARY",
  "amount": "500000.00",
  "description": "Monthly salary",
  "date": "2024-01-15"
}
```

**Success Response (201 Created):** Income object

**Source Options:** `SALARY`, `BUSINESS`, `SIDE-HUSTLES`, `OTHERS`

---

### 3. Get Income Details

**Endpoint:** `GET /income/<id>/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):** Income object

---

### 4. Update Income

**Endpoint:** `PUT /income/<id>/`

**Authentication:** Required (Bearer Token)

**Request Body:** Same as create income

**Success Response (200 OK):** Updated income object

---

### 5. Delete Income

**Endpoint:** `DELETE /income/<id>/`

**Authentication:** Required (Bearer Token)

**Success Response (204 No Content):** Empty body

---

### 6. List Expenses

**Endpoint:** `GET /expenses/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):**

```json
[
  {
    "id": 1,
    "category": "FOOD",
    "amount": "50000.00",
    "description": "Groceries",
    "date": "2024-01-15",
    "owner": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

**Note:** Only returns expenses for authenticated user

---

### 7. Create Expense

**Endpoint:** `POST /expenses/`

**Authentication:** Required (Bearer Token)

**Request Body:**

```json
{
  "category": "FOOD",
  "amount": "50000.00",
  "description": "Groceries",
  "date": "2024-01-15"
}
```

**Success Response (201 Created):** Expense object

**Category Options:** `ONLINE_SERVICES`, `TRAVEL`, `FOOD`, `RENT`, `OTHERS`

---

### 8. Get Expense Details

**Endpoint:** `GET /expenses/<id>/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):** Expense object

---

### 9. Update Expense

**Endpoint:** `PUT /expenses/<id>/`

**Authentication:** Required (Bearer Token)

**Request Body:** Same as create expense

**Success Response (200 OK):** Updated expense object

---

### 10. Delete Expense

**Endpoint:** `DELETE /expenses/<id>/`

**Authentication:** Required (Bearer Token)

**Success Response (204 No Content):** Empty body

---

### 11. List All Expenses

**Endpoint:** `GET /expenses/all/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):** Array of all expense objects

---

## Results/CSV Data

### 1. Upload CSV (Admin Only)

**Endpoint:** `POST /results/upload/`

**Authentication:** Required (Bearer Token + Admin)

**Content-Type:** `multipart/form-data`

**Request Body:**

```json
{
  "csv_file": "CSV file",
  "name": "Dividend Data 2024",
  "data_type": "dividends",
  "description": "Annual dividend data",
  "upload_date": "2024-01-01",
  "status": "pending"
}
```

**Success Response (201 Created):**

```json
{
  "id": 1,
  "name": "Dividend Data 2024",
  "slug": "dividend-data-2024",
  "data_type": "dividends",
  "description": "Annual dividend data",
  "upload_date": "2024-01-01",
  "status": "pending",
  "json_data": [
    {
      "Company": "ABC Corp",
      "Dividend": "100.50",
      "Date": "2024-01-01"
    }
  ],
  "uploaded_by": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Notes:**

- CSV file is automatically parsed to JSON
- Supports multiple encodings (UTF-8, Latin-1)
- Status options: `pending`, `approved`, `disapproved`

---

### 2. Update CSV Upload (Admin Only)

**Endpoint:** `PUT /results/nmdata/<pk>/update/`

**Authentication:** Required (Bearer Token + Admin)

**Content-Type:** `multipart/form-data`

**Request Body:** Same as upload CSV (all fields optional for PATCH)

**Success Response (200 OK):** Updated NMData object

---

### 3. Get User's Uploads

**Endpoint:** `GET /results/my-uploads/`

**Authentication:** Required (Bearer Token)

**Success Response (200 OK):** Array of NMData objects uploaded by authenticated user

---

### 4. View All Uploads

**Endpoint:** `GET /results/uploads/`

**Authentication:** Not Required

**Query Parameters:**

- `name` - Filter by name (icontains)
- `data_type` - Filter by data type (icontains)
- `company` - Filter by company within JSON data
- `sort_by` - Sort results (default: `-upload_date`)
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10, max: 100)

**Success Response (200 OK):**

```json
{
  "count": 100,
  "next": "http://localhost:8000/results/uploads/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Dividend Data 2024",
      "data_type": "dividends",
      "description": "Annual dividend data",
      "upload_date": "2024-01-01",
      "status": "approved",
      "uploaded_by": 1,
      "json_data": [
        {
          "Company": "ABC Corp",
          "Dividend": "100.50",
          "Date": "2024-01-01"
        }
      ]
    }
  ]
}
```

**Notes:**

- When `company` filter is used, only matching rows from `json_data` are returned
- Pagination is applied automatically

---

## Error Responses

### Standard Error Format

```json
{
  "error": "Error message description",
  "detail": "Additional details (if available)"
}
```

### Common HTTP Status Codes

| Status Code                 | Meaning                                    |
| --------------------------- | ------------------------------------------ |
| `200 OK`                    | Request successful                         |
| `201 Created`               | Resource created successfully              |
| `204 No Content`            | Request successful, no content to return   |
| `400 Bad Request`           | Invalid request data                       |
| `401 Unauthorized`          | Authentication required or failed          |
| `403 Forbidden`             | Permission denied (not admin or not owner) |
| `404 Not Found`             | Resource not found                         |
| `500 Internal Server Error` | Server error                               |

---

## Authentication Header Format

All protected endpoints require the following header:

```
Authorization: Bearer <access_token>
```

**Example:**

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

## Data Models

### User Model

| Field           | Type     | Description                     |
| --------------- | -------- | ------------------------------- |
| `id`            | Integer  | Unique identifier               |
| `username`      | String   | Auto-generated username         |
| `email`         | String   | User's email address (unique)   |
| `firstname`     | String   | First name                      |
| `lastname`      | String   | Last name                       |
| `address`       | String   | Physical address (optional)     |
| `phone`         | String   | Phone number (optional)         |
| `linkedin`      | String   | LinkedIn profile URL (optional) |
| `referral_code` | String   | Unique referral code            |
| `is_verified`   | Boolean  | Email verification status       |
| `is_approved`   | Boolean  | Admin approval status           |
| `is_staff`      | Boolean  | Admin privileges                |
| `is_active`     | Boolean  | Account active status           |
| `created_at`    | DateTime | Account creation timestamp      |
| `updated_at`    | DateTime | Last update timestamp           |

### Investment Model

| Field                 | Type        | Description                     |
| --------------------- | ----------- | ------------------------------- |
| `id`                  | Integer     | Unique identifier               |
| `name`                | String      | Investment name                 |
| `slug`                | String      | URL-friendly identifier         |
| `description`         | Text        | Investment description          |
| `location`            | String      | Investment location             |
| `amount`              | Integer     | Investment amount               |
| `project_cost`        | Integer     | Total project cost              |
| `project_raise`       | Integer     | Amount to raise                 |
| `roi`                 | Decimal     | Return on investment percentage |
| `annualized`          | Decimal     | Annualized return               |
| `currency`            | Foreign Key | Currency reference              |
| `dealtype`            | Foreign Key | Deal type reference             |
| `room`                | Foreign Key | Investment room reference       |
| `period`              | Foreign Key | Investment period reference     |
| `risk`                | Foreign Key | Risk level reference            |
| `volume`              | Integer     | Available units                 |
| `only_returns`        | Boolean     | Returns only option             |
| `off_plan`            | Boolean     | Off-plan option                 |
| `outright_purchase`   | Boolean     | Outright purchase option        |
| `offer_price`         | Integer     | Offer price                     |
| `spot_price`          | Integer     | Spot price                      |
| `unit_price`          | Integer     | Unit price                      |
| `is_verified`         | Boolean     | Admin verification status       |
| `is_closed`           | Boolean     | Investment closed status        |
| `title_status`        | String      | Title status                    |
| `construction_status` | String      | Construction status             |
| `project_status`      | String      | Project status                  |
| `start_date`          | Date        | Investment start date           |
| `end_date`            | Date        | Investment end date             |
| `offer_period`        | Date        | Offer period end date           |
| `milestone`           | Integer     | Current milestone               |
| `minimum_allotment`   | Integer     | Minimum investment              |
| `maximum_allotment`   | Integer     | Maximum investment              |
| `features`            | Text        | Investment features             |
| `video`               | String      | Video URL                       |
| `owner`               | Foreign Key | User who created investment     |
| `created_at`          | DateTime    | Creation timestamp              |
| `updated_at`          | DateTime    | Last update timestamp           |

### Investors Model

| Field             | Type        | Description                                           |
| ----------------- | ----------- | ----------------------------------------------------- |
| `id`              | Integer     | Unique identifier                                     |
| `investment`      | Foreign Key | Investment reference                                  |
| `investor`        | Foreign Key | User who invested                                     |
| `amount`          | Integer     | Investment amount                                     |
| `bid_price`       | Integer     | Bid price                                             |
| `house_number`    | String      | Unit/house number                                     |
| `slug`            | String      | URL-friendly identifier                               |
| `investment_type` | String      | Type: `only returns`, `off plan`, `outright purchase` |
| `volume`          | Integer     | Number of units                                       |
| `payment`         | String      | Payment status: `not started`, `partial`, `full`      |
| `serialkey`       | String      | Unique serial key                                     |
| `is_approved`     | Boolean     | Admin approval status                                 |
| `approved_by`     | Foreign Key | Admin who approved                                    |
| `is_closed`       | Boolean     | Investment closed status                              |
| `closed_by`       | Foreign Key | Admin who closed                                      |
| `created_at`      | DateTime    | Creation timestamp                                    |
| `updated_at`      | DateTime    | Last update timestamp                                 |

### Installment Model

| Field         | Type        | Description                     |
| ------------- | ----------- | ------------------------------- |
| `id`          | Integer     | Unique identifier               |
| `investor`    | Foreign Key | Investor subscription reference |
| `amount`      | Integer     | Installment amount              |
| `serialkey`   | String      | Unique serial key               |
| `is_approved` | Boolean     | Admin approval status           |
| `approved_by` | Foreign Key | Admin who approved              |
| `created_at`  | DateTime    | Creation timestamp              |
| `updated_at`  | DateTime    | Last update timestamp           |

### Article Model

| Field            | Type        | Description                      |
| ---------------- | ----------- | -------------------------------- |
| `id`             | Integer     | Unique identifier                |
| `title`          | String      | Article title                    |
| `slug`           | String      | URL-friendly identifier          |
| `content`        | Text        | Article content (HTML supported) |
| `author`         | Foreign Key | User who created article         |
| `featured_image` | Image       | Featured image (optional)        |
| `created_at`     | DateTime    | Creation timestamp               |
| `updated_at`     | DateTime    | Last update timestamp            |

### Comment Model

| Field          | Type        | Description                                |
| -------------- | ----------- | ------------------------------------------ |
| `id`           | Integer     | Unique identifier                          |
| `slug`         | String      | URL-friendly identifier                    |
| `comment`      | Text        | Comment content                            |
| `investment`   | Foreign Key | Investment reference (optional)            |
| `investor`     | Foreign Key | Investor subscription reference (optional) |
| `responded_by` | Foreign Key | User who responded                         |
| `is_closed`    | Boolean     | Comment closed status                      |
| `created_at`   | DateTime    | Creation timestamp                         |
| `updated_at`   | DateTime    | Last update timestamp                      |

### Income Model

| Field         | Type        | Description                                                   |
| ------------- | ----------- | ------------------------------------------------------------- |
| `id`          | Integer     | Unique identifier                                             |
| `source`      | String      | Income source: `SALARY`, `BUSINESS`, `SIDE-HUSTLES`, `OTHERS` |
| `amount`      | Decimal     | Income amount                                                 |
| `description` | Text        | Income description                                            |
| `owner`       | Foreign Key | User who owns income                                          |
| `date`        | Date        | Income date                                                   |
| `created_at`  | DateTime    | Creation timestamp                                            |
| `updated_at`  | DateTime    | Last update timestamp                                         |

### Expense Model

| Field         | Type        | Description                                                             |
| ------------- | ----------- | ----------------------------------------------------------------------- |
| `id`          | Integer     | Unique identifier                                                       |
| `category`    | String      | Expense category: `ONLINE_SERVICES`, `TRAVEL`, `FOOD`, `RENT`, `OTHERS` |
| `amount`      | Decimal     | Expense amount                                                          |
| `description` | Text        | Expense description                                                     |
| `owner`       | Foreign Key | User who owns expense                                                   |
| `date`        | Date        | Expense date                                                            |
| `created_at`  | DateTime    | Creation timestamp                                                      |
| `updated_at`  | DateTime    | Last update timestamp                                                   |

### NMData Model

| Field         | Type        | Description                                  |
| ------------- | ----------- | -------------------------------------------- |
| `id`          | Integer     | Unique identifier                            |
| `name`        | String      | CSV upload name                              |
| `slug`        | String      | URL-friendly identifier                      |
| `data_type`   | String      | Type of data                                 |
| `description` | Text        | Upload description                           |
| `upload_date` | Date        | Upload date                                  |
| `csv_file`    | File        | CSV file                                     |
| `status`      | String      | Status: `pending`, `approved`, `disapproved` |
| `json_data`   | JSON        | Parsed CSV data                              |
| `uploaded_by` | Foreign Key | User who uploaded                            |
| `created_at`  | DateTime    | Creation timestamp                           |
| `updated_at`  | DateTime    | Last update timestamp                        |

---

## Notes for Frontend Developers

### 1. Token Storage

- Store the `access` token in memory (or httpOnly cookie) and `refresh` token securely
- The access token expires after 30 minutes
- Implement automatic token refresh using the `/auth/refresh/` endpoint

### 2. Email Verification

- Newly registered users must verify their email before they can log in
- The login endpoint will return `401 Unauthorized: Email is not verified` until verification is complete
- Email verification link includes a JWT token

### 3. User Approval

- Users may need admin approval (`is_approved: true`) to access certain features
- Check the `is_approved` field in the login response
- Some investment operations require user approval

### 4. CORS

- The API is configured to accept requests from common frontend development ports (3000, 5173, etc.)
- If your frontend runs on a different port, ask the backend dev to add it to `CORS_ORIGIN_WHITELIST`

### 5. File Uploads

- Use `multipart/form-data` content type for file uploads
- Multiple images can be uploaded for investments (gallery, galleries_1-4)
- CSV files for investor uploads must follow the specified format

### 6. Pagination

- List endpoints support pagination
- Use `page` and `page_size` query parameters
- Response includes `count`, `next`, and `previous` links

### 7. Filtering and Searching

- Many endpoints support filtering via query parameters
- Use `search` parameter for text-based searches
- Use specific field names for exact filtering

### 8. Error Handling

- Always check HTTP status codes
- Handle 401 Unauthorized by refreshing tokens or redirecting to login
- Display user-friendly error messages from response body

### 9. Investment Workflow

1. User browses investments
2. User subscribes to investment (creates Investors record)
3. Admin approves subscription
4. User can add installments (if partial payment)
5. Admin approves installments
6. Investment can be closed when complete

### 10. CSV Data Management

- CSV files are automatically parsed to JSON
- Supports multiple encodings
- Filter by company name within JSON data
- Paginated results for large datasets

### 11. Swagger UI

- Access interactive API documentation at `/` when backend is running
- Test endpoints directly from Swagger UI
- View request/response schemas

### 12. Rate Limiting

- Be aware of potential rate limits on certain endpoints
- Implement retry logic with exponential backoff for failed requests
- Cache responses where appropriate

### 13. Date Formats

- Use ISO 8601 format for date fields: `YYYY-MM-DD`
- Use ISO 8601 format for datetime fields: `YYYY-MM-DDTHH:MM:SSZ`

### 14. Currency Handling

- All monetary values are in integers (no decimal places)
- Display values formatted with appropriate currency symbols
- ROI and annualized returns are decimals (2 decimal places)

### 15. Investment Types

- `only returns`: Invest for returns only
- `off plan`: Off-plan purchase
- `outright purchase`: Full outright purchase

### 16. Payment Status

- `not started`: No payments made
- `partial`: Partial payments made
- `full`: Full payment completed

---

## API Base URL Structure

```
http://localhost:8000/
├── auth/              # Authentication & user management
├── investment/        # Investment operations
├── investor/          # Investor operations
├── article/           # Blog/articles
├── comment/           # Comments system
├── income/            # Income tracking (commented out)
├── expenses/          # Expense tracking
├── results/           # CSV data management
├── api/token/         # JWT token endpoints
└── /                 # Swagger UI documentation
```

---

## Quick Start Examples

### Login and Get Token

```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

### Get Investments

```bash
curl -X GET http://localhost:8000/investment/investment/ \
  -H "Authorization: Bearer <access_token>"
```

### Subscribe to Investment

```bash
curl -X POST http://localhost:8000/investor/investment/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000000, "bid_price": 1050000, "volume": 1, "investment_type": "only returns"}'
```

### Create Article

```bash
curl -X POST http://localhost:8000/article/posts/create/ \
  -H "Authorization: Bearer <access_token>" \
  -F "title=Investment Guide" \
  -F "content=<p>Guide content...</p>" \
  -F "featured_image=@image.jpg"
```

---

**Last Updated:** 2026-03-05

**API Version:** v1

**Contact:** info@nairametrics.com
