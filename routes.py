from fastapi import APIRouter, HTTPException, Body, Form, Header, Query
from typing import Dict, Any, Optional
from datetime import datetime
import secrets
import uuid

# Initialize router
router = APIRouter()

@router.post("/api/upload_prd")
async def upload_prd(request: Dict[str, Any] = Body(...)):
    """
    Mock endpoint for PRD upload
    
    Accepts:
    - text: Combined text from textarea and/or extracted from uploaded file
    - source: Origin of the text (e.g., "textarea" or "file: filename.pdf")
    
    Returns:
    - 200 status code on success
    - Error message on failure
    """
    
    # Extract fields from request dictionary
    text = request.get("text", "")
    source = request.get("source", "textarea")
    
    # Validate that text is not empty
    if not text or len(text.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="PRD text cannot be empty"
        )
    
    # Return 200 status code (empty response body)
    return {}


@router.post("/api/v1/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """
    Mock login endpoint
    
    Accepts:
    - username: User's email address (sent as form data)
    - password: User's password (sent as form data)
    
    Returns:
    - access_token: JWT-like mock token
    - token_type: Bearer
    - user: User object with email, name, and id
    """
    
    # For mock purposes, accept any non-empty credentials
    if not username or not password:
        raise HTTPException(
            status_code=400,
            detail="Username and password are required"
        )
    
    # Mock validation - in real app, verify credentials against database
    # For now, reject only if password is too short
    if len(password) < 3:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    # Generate a mock JWT-like token
    mock_token = f"mock_jwt_{secrets.token_urlsafe(32)}"
    
    # Extract name from email
    user_name = username.split('@')[0] if '@' in username else username
    
    # Create mock user object
    user_data = {
        "id": f"user_{secrets.token_hex(8)}",
        "email": username,
        "name": user_name.capitalize(),
        "is_verified": True,
        "created_at": datetime.now().isoformat(),
    }
    
    return {
        "access_token": mock_token,
        "token_type": "bearer",
        "user": user_data
    }
####################################################################################
# Projects - Dashboard.jsx
####################################################################################

# Mock projects data store (in-memory)
MOCK_PROJECTS = [
    {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "name": "E-commerce Platform",
        "description": "B2B e-commerce solution with advanced inventory management and real-time analytics",
        "created_at": "2025-10-01T09:15:30.000Z",
        "updated_at": "2025-10-05T14:22:15.000Z"
    },
    {
        "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
        "name": "Customer Portal",
        "description": "Self-service portal for customer account management",
        "created_at": "2025-09-28T11:30:00.000Z",
        "updated_at": "2025-10-04T16:45:22.000Z"
    },
    {
        "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
        "name": "Internal Dashboard",
        "description": "Analytics dashboard for business intelligence and reporting",
        "created_at": "2025-09-25T08:00:00.000Z",
        "updated_at": "2025-10-03T10:15:30.000Z"
    },
    {
        "id": "d4e5f6a7-b8c9-0123-def1-234567890123",
        "name": "Mobile App Backend",
        "description": "RESTful API backend for iOS and Android applications",
        "created_at": "2025-09-20T14:20:00.000Z",
        "updated_at": "2025-10-02T09:30:45.000Z"
    },
    {
        "id": "e5f6a7b8-c9d0-1234-ef12-345678901234",
        "name": "Payment Gateway Integration",
        "description": "Secure payment processing system with multiple payment providers",
        "created_at": "2025-09-15T10:45:00.000Z",
        "updated_at": "2025-10-01T13:20:10.000Z"
    },
    {
        "id": "f6a7b8c9-d0e1-2345-f123-456789012345",
        "name": "Inventory Management System",
        "description": None,
        "created_at": "2025-09-10T16:30:00.000Z",
        "updated_at": "2025-09-30T11:55:22.000Z"
    }
]


def verify_auth_token(authorization: Optional[str] = None):
    """
    Mock authentication verification
    Checks if Authorization header is present and valid
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    
    token = authorization.replace("Bearer ", "")
    
    # Mock token validation - check if token is not empty and has minimum length
    if not token or len(token) < 10:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    
    # Mock expired token check (if token contains 'expired')
    if "expired" in token.lower():
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    
    return True


@router.get("/api/v1/projects")
async def list_projects(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    size: int = Query(50, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query for project name or description"),
    authorization: Optional[str] = Header(None)
):
    """
    List all projects with pagination and search support
    
    Query Parameters:
    - page: Page number (default: 1)
    - size: Items per page (default: 50, max: 100)
    - search: Optional search term to filter projects
    
    Returns:
    - projects: List of project objects
    - total: Total number of projects
    - page: Current page number
    - size: Items per page
    - pages: Total number of pages
    """
    
    # Verify authentication
    verify_auth_token(authorization)
    
    # Filter projects based on search query
    filtered_projects = MOCK_PROJECTS.copy()
    
    if search and search.strip():
        search_term = search.strip().lower()
        filtered_projects = [
            p for p in filtered_projects
            if search_term in p["name"].lower() or 
            (p["description"] and search_term in p["description"].lower())
        ]
    
    # Calculate pagination
    total = len(filtered_projects)
    pages = (total + size - 1) // size if total > 0 else 0
    
    # Get paginated results
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_projects = filtered_projects[start_idx:end_idx]
    
    return {
        "projects": paginated_projects,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


@router.post("/api/v1/projects", status_code=201)
async def create_project(
    request: Dict[str, Any] = Body(...),
    authorization: Optional[str] = Header(None)
):
    """
    Create a new project
    
    Request Body:
    - name: Project name (required, 1-255 characters)
    - description: Project description (optional, 0-1000 characters)
    
    Returns:
    - id: Generated UUID for the project
    - name: Project name
    - description: Project description (or null)
    - created_at: ISO 8601 timestamp
    - updated_at: ISO 8601 timestamp
    """
    
    # Verify authentication
    verify_auth_token(authorization)
    
    # Validate required fields
    if "name" not in request:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing"
            }]
        )
    
    name = request.get("name")
    description = request.get("description")
    
    # Validate name is a string
    if not isinstance(name, str):
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": ["body", "name"],
                "msg": "str type expected",
                "type": "type_error.str"
            }]
        )
    
    # Trim whitespace
    name = name.strip()
    
    # Validate name is not empty
    if not name:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": ["body", "name"],
                "msg": "Project name cannot be empty",
                "type": "value_error"
            }]
        )
    
    # Validate name length
    if len(name) > 255:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": ["body", "name"],
                "msg": "ensure this value has at most 255 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {
                    "limit_value": 255
                }
            }]
        )
    
    # Validate description if provided
    if description is not None:
        if not isinstance(description, str):
            raise HTTPException(
                status_code=400,
                detail=[{
                    "loc": ["body", "description"],
                    "msg": "str type expected",
                    "type": "type_error.str"
                }]
            )
        
        # Trim whitespace
        description = description.strip()
        
        # Convert empty string to None
        if not description:
            description = None
        
        # Validate description length
        if description and len(description) > 1000:
            raise HTTPException(
                status_code=400,
                detail=[{
                    "loc": ["body", "description"],
                    "msg": "ensure this value has at most 1000 characters",
                    "type": "value_error.any_str.max_length",
                    "ctx": {
                        "limit_value": 1000
                    }
                }]
            )
    
    # Check for duplicate project name (case-insensitive)
    for project in MOCK_PROJECTS:
        if project["name"].lower() == name.lower():
            raise HTTPException(
                status_code=409,
                detail="A project with this name already exists"
            )
    
    # Generate new project
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    new_project = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "created_at": now,
        "updated_at": now
    }
    
    # Add to mock data store
    MOCK_PROJECTS.insert(0, new_project)
    
    return new_project

#######################################################################################
## PRD.jsx###########################################################################
#######################################################################################

@router.get("/api/get_prd")
async def get_prd(
    user_id: str = Query(..., description="User ID"),
    project_id: str = Query(..., description="Project ID"),
    authorization: Optional[str] = Header(None)
):
    """
    Get PRD text for a specific project
    
    Query Parameters:
    - user_id: User ID (required)
    - project_id: Project ID (required)
    
    Returns:
    - text: PRD text if project_id matches, otherwise empty string
    """
    
    # Verify authentication
    verify_auth_token(authorization)
    
    # Check if project_id matches the specific one
    if project_id == "b2c3d4e5-f6a7-8901-bcde-f12345678901":
        return {
            "text": "Build me a Restaurant dine in reservation system that gamifies coupons"
        }
    else:
        return {
            "text": ""
        }
#######################################################################################
## UserPersona.jsx###########################################################################
#######################################################################################
@router.get("/api/get_userpersonas")
async def get_userpersonas(
    user_id: Optional[str] = None,
    project_id: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    """
    Mock endpoint for getting user personas
    
    Query Parameters:
    - user_id: ID of the user (optional)
    - project_id: ID of the project (optional)
    
    Headers:
    - Authorization: Bearer token (automatically sent by frontend)
    
    Returns:
    - success: Boolean indicating if request was successful
    - personas: List of user personas (empty if none exist)
    """
    
    # Extract token from Authorization header
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    
    # Log the incoming request for debugging
    print(f"\n📥 Get User Personas Request:")
    print(f"   🔑 Token: {token[:20] + '...' if token else 'None'}")
    print(f"   👤 User ID: {user_id}")
    print(f"   📁 Project ID: {project_id}\n")
    
    # For demonstration, return empty personas 50% of the time
    # You can change this logic based on your needs
    import random
    
    # Uncomment line below to always return data for testing
    # has_personas = True
    
    # Uncomment line below to always return empty for testing
    # has_personas = False
    
    # Random behavior for testing both scenarios
    has_personas = random.choice([True, False])
    has_personas = True
    if has_personas:
        # Return mock personas when data exists
        mock_personas = [
            {
                "id": "persona-1",
                "name": "System Administrator",
                "description": "Manages user accounts, system configurations, and monitors platform health. Requires comprehensive dashboard with admin controls.",
                "goals": ["Efficient user management", "System monitoring", "Access control"],
                "painPoints": ["Complex configuration processes", "Limited visibility into system health"],
                "keyFeatures": ["User management dashboard", "System analytics", "Role-based access control"]
            },
            {
                "id": "persona-2",
                "name": "Business Analyst",
                "description": "Analyzes business data, generates reports, and makes data-driven decisions. Needs intuitive analytics and reporting tools.",
                "goals": ["Data visualization", "Report generation", "Trend analysis"],
                "painPoints": ["Difficulty in accessing real-time data", "Complex reporting interfaces"],
                "keyFeatures": ["Interactive dashboards", "Custom report builder", "Data export capabilities"]
            },
            {
                "id": "persona-3",
                "name": "End User/Customer",
                "description": "Primary user of the application who interacts with core features. Expects simple, intuitive interface with quick task completion.",
                "goals": ["Quick task completion", "Easy navigation", "Reliable service"],
                "painPoints": ["Complicated workflows", "Slow response times"],
                "keyFeatures": ["Streamlined workflows", "Quick actions", "Responsive interface"]
            },
            {
                "id": "persona-4",
                "name": "Developer/Technical User",
                "description": "Integrates systems, manages APIs, and customizes functionality. Requires technical documentation and developer tools.",
                "goals": ["API integration", "System customization", "Technical documentation"],
                "painPoints": ["Poor API documentation", "Limited customization options"],
                "keyFeatures": ["API documentation", "Developer console", "Webhook management"]
            }
        ]
        
        return {
            "success": True,
            "personas": mock_personas,
            "message": "User personas retrieved successfully"
        }
    else:
        # Return empty personas
        return {
            "success": True,
            "personas": [],
            "message": "No user personas found"
        }


@router.post("/api/upload_userpersonas")
async def upload_userpersonas(
    request: Dict[str, Any] = Body(...),
    authorization: Optional[str] = Header(None)
):
    """
    Mock endpoint for uploading selected user personas
    
    Accepts:
    - selected_personas: List of selected persona objects
    - user_id: ID of the user (optional)
    - project_id: ID of the project (optional)
    
    Headers:
    - Authorization: Bearer token (automatically sent by frontend)
    
    Returns:
    - success: Boolean indicating if upload was successful
    - message: Human-readable message
    - data: Saved personas data
    """
    
    # Extract fields from request dictionary
    selected_personas = request.get("selected_personas", [])
    user_id = request.get("user_id")
    project_id = request.get("project_id")
    
    # Extract token from Authorization header
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    
    # Log the incoming request for debugging
    print(f"\n📤 Upload User Personas Request:")
    print(f"   🔑 Token: {token[:20] + '...' if token else 'None'}")
    print(f"   👤 User ID: {user_id}")
    print(f"   📁 Project ID: {project_id}")
    print(f"   👥 Selected Personas Count: {len(selected_personas)}")
    print(f"   📋 Personas: {[p.get('name', 'Unknown') for p in selected_personas]}\n")
    
    # Validate that at least one persona is selected
    if not selected_personas or len(selected_personas) == 0:
        raise HTTPException(
            status_code=400,
            detail="At least one persona must be selected"
        )
    print(f"   👥 Selected Personas: {selected_personas}")
    # Mock response data
    response_data = {
        "personas_saved": selected_personas,
        "count": len(selected_personas),
        "user_id": user_id,
        "project_id": project_id,
        "saved_at": datetime.now().isoformat(),
        "next_step": "brand_design"
    }
    
    return {
        "success": True,
        "message": f"Successfully saved {len(selected_personas)} user persona(s)",
        "data": response_data
    }
####    #############
## BrandDesign.jsx###########################################################################
#######################################################################################
@router.get("/api/get_branddesign")
async def get_branddesign(
    user_id: Optional[str] = None,
    project_id: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    """
    Mock endpoint for getting brand design configuration
    
    Query Parameters:
    - user_id: ID of the user (optional)
    - project_id: ID of the project (optional)
    
    Headers:
    - Authorization: Bearer token (automatically sent by frontend)
    
    Returns:
    - Brand design data or empty object if no data exists
    """
    
    # Extract token from Authorization header
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    
    # Log the incoming request for debugging
    print(f"\n📥 Get Brand Design Request:")
    print(f"   🔑 Token: {token[:20] + '...' if token else 'None'}")
    print(f"   👤 User ID: {user_id}")
    print(f"   📁 Project ID: {project_id}\n")
    
    # For demonstration, return empty brand design 50% of the time
    # You can change this logic based on your needs
    import random
    
    # Uncomment line below to always return data for testing
    # has_brand_design = True
    
    # Uncomment line below to always return empty for testing (use defaults)
    # has_brand_design = False
    
    # Random behavior for testing both scenarios
    has_brand_design = random.choice([True, False])
    
    if has_brand_design:
        # Return mock brand design when data exists
        mock_brand_design = {
            "brandName": "TechCorp Solutions",
            "logoUrl": None,  # No logo uploaded
            "colors": {
                "primary": "#3B82F6",     # Blue
                "secondary": "#1E293B",   # Dark slate
                "accent": "#8B5CF6",      # Purple
                "background": "#0F172A",  # Very dark blue
                "foreground": "#F8FAFC"   # Off-white
            },
            "fontFamily": "Inter",
            "brandVoice": "Innovation Through Technology",
            "tone": "Professional",
            "timestamp": datetime.now().isoformat()
        }
        
        print("   ✅ Returning saved brand design data")
        return mock_brand_design
    else:
        # Return empty object - frontend will use defaults (black, orange, white with Montserrat)
        print("   ⚠️  No brand design found - frontend will use defaults")
        return {}


@router.post("/api/upload_branddesign")
async def upload_branddesign(
    request: Dict[str, Any] = Body(...),
    authorization: Optional[str] = Header(None)
):
    """
    Mock endpoint for uploading/saving brand design configuration
    
    Accepts:
    - brandName: Brand name
    - logoUrl: Logo URL or base64 (optional)
    - colors: Object with primary, secondary, accent, background, foreground colors
    - fontFamily: Font family name
    - brandVoice: Brand voice/tagline
    - tone: Brand tone
    - user_id: ID of the user (optional)
    - project_id: ID of the project (optional)
    
    Headers:
    - Authorization: Bearer token (automatically sent by frontend)
    
    Returns:
    - success: Boolean indicating if upload was successful
    - message: Human-readable message
    - data: Saved brand design data
    """
    
    # Extract fields from request dictionary
    brand_name = request.get("brandName", "")
    logo_url = request.get("logoUrl")
    colors = request.get("colors", {})
    font_family = request.get("fontFamily", "")
    brand_voice = request.get("brandVoice", "")
    tone = request.get("tone", "")
    user_id = request.get("user_id")
    project_id = request.get("project_id")
    
    # Extract token from Authorization header
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    
    # Log the incoming request for debugging
    print(f"\n📤 Upload Brand Design Request:")
    print(f"   🔑 Token: {token[:20] + '...' if token else 'None'}")
    print(f"   👤 User ID: {user_id}")
    print(f"   📁 Project ID: {project_id}")
    print(f"   🎨 Brand Name: {brand_name}")
    print(f"   🎨 Font Family: {font_family}")
    print(f"   🎨 Brand Voice: {brand_voice}")
    print(f"   🎨 Tone: {tone}")
    print(f"   🎨 Colors: {colors}\n")
    
    # Validate required fields
    if not brand_name or len(brand_name.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Brand name is required"
        )
    
    if not colors:
        raise HTTPException(
            status_code=400,
            detail="Brand colors are required"
        )
    
    # Mock response data
    response_data = {
        "brandName": brand_name,
        "logoUrl": logo_url,
        "colors": colors,
        "fontFamily": font_family,
        "brandVoice": brand_voice,
        "tone": tone,
        "user_id": user_id,
        "project_id": project_id,
        "saved_at": datetime.now().isoformat(),
        "next_step": "business_logic"
    }
    
    print("   ✅ Brand design saved successfully")
    
    return {
        "success": True,
        "message": "Brand design saved successfully",
        "data": response_data
    }
####################################################################################
#ThirdParty Api Call
####################################################################################

# Providers mapping for each third-party API category
PROVIDERS_JSON = {
    "payment": [
        {"name": "Stripe", "description": "Complete payment platform with extensive features"},
        {"name": "PayPal", "description": "Widely recognized payment solution"},
        {"name": "Square", "description": "Payment processing for businesses of all sizes"},
        {"name": "Braintree", "description": "PayPal-owned payment gateway"},
        {"name": "Authorize.Net", "description": "Established payment gateway solution"}
    ],
    "maps": [
        {"name": "Google Maps", "description": "Comprehensive mapping and location services"},
        {"name": "Mapbox", "description": "Customizable maps and location data"},
        {"name": "HERE Maps", "description": "Enterprise-grade mapping solution"},
        {"name": "OpenStreetMap", "description": "Open-source collaborative mapping"},
        {"name": "Azure Maps", "description": "Microsoft's mapping and geospatial services"}
    ],
    "oauth": [
        {"name": "Auth0", "description": "Identity platform for authentication and authorization"},
        {"name": "Okta", "description": "Enterprise identity and access management"},
        {"name": "Firebase Auth", "description": "Google's authentication solution"},
        {"name": "AWS Cognito", "description": "Amazon's user identity and authentication"},
        {"name": "Keycloak", "description": "Open-source identity and access management"}
    ],
    "sms": [
        {"name": "Twilio", "description": "Leading cloud communications platform"},
        {"name": "AWS SNS", "description": "Amazon's messaging and notification service"},
        {"name": "Vonage (Nexmo)", "description": "Communication APIs for SMS and voice"},
        {"name": "Plivo", "description": "Cloud communication platform"},
        {"name": "MessageBird", "description": "Omnichannel communication platform"}
    ],
    "email": [
        {"name": "SendGrid", "description": "Twilio's email delivery platform"},
        {"name": "AWS SES", "description": "Amazon's email sending service"},
        {"name": "Mailgun", "description": "Email automation service for developers"},
        {"name": "Postmark", "description": "Fast and reliable transactional email"},
        {"name": "Resend", "description": "Modern email API for developers"}
    ],
    "storage": [
        {"name": "AWS S3", "description": "Amazon's scalable object storage"},
        {"name": "Google Cloud Storage", "description": "Google's unified object storage"},
        {"name": "Azure Blob Storage", "description": "Microsoft's object storage solution"},
        {"name": "Cloudinary", "description": "Media management and optimization platform"},
        {"name": "Backblaze B2", "description": "Cost-effective cloud storage"}
    ],
    "messaging": [
        {"name": "Firebase Cloud Messaging", "description": "Google's cross-platform messaging solution"},
        {"name": "OneSignal", "description": "Multi-channel customer engagement platform"},
        {"name": "Pusher", "description": "Real-time messaging and push notifications"},
        {"name": "AWS SNS", "description": "Amazon's pub/sub messaging service"},
        {"name": "PubNub", "description": "Real-time communication platform"}
    ]
}

# Provider documentation URLs
PROVIDER_DOCUMENTATION = {
    # Payment providers
    "Stripe": "https://stripe.com/docs/api",
    "PayPal": "https://developer.paypal.com/docs/api/overview/",
    "Square": "https://developer.squareup.com/reference/square",
    "Braintree": "https://developer.paypal.com/braintree/docs",
    "Authorize.Net": "https://developer.authorize.net/api/reference/",
    
    # Maps providers
    "Google Maps": "https://developers.google.com/maps/documentation",
    "Mapbox": "https://docs.mapbox.com/api/overview/",
    "HERE Maps": "https://developer.here.com/documentation",
    "OpenStreetMap": "https://wiki.openstreetmap.org/wiki/API",
    "Azure Maps": "https://docs.microsoft.com/en-us/azure/azure-maps/",
    
    # OAuth providers
    "Auth0": "https://auth0.com/docs/api",
    "Okta": "https://developer.okta.com/docs/reference/",
    "Firebase Auth": "https://firebase.google.com/docs/auth",
    "AWS Cognito": "https://docs.aws.amazon.com/cognito/",
    "Keycloak": "https://www.keycloak.org/documentation",
    
    # SMS providers
    "Twilio": "https://www.twilio.com/docs/sms",
    "AWS SNS": "https://docs.aws.amazon.com/sns/",
    "Vonage (Nexmo)": "https://developer.vonage.com/messaging/sms/overview",
    "Plivo": "https://www.plivo.com/docs/sms/",
    "MessageBird": "https://developers.messagebird.com/api/sms-messaging/",
    
    # Email providers
    "SendGrid": "https://docs.sendgrid.com/api-reference",
    "AWS SES": "https://docs.aws.amazon.com/ses/",
    "Mailgun": "https://documentation.mailgun.com/en/latest/api_reference.html",
    "Postmark": "https://postmarkapp.com/developer",
    "Resend": "https://resend.com/docs",
    
    # Storage providers
    "AWS S3": "https://docs.aws.amazon.com/s3/",
    "Google Cloud Storage": "https://cloud.google.com/storage/docs",
    "Azure Blob Storage": "https://docs.microsoft.com/en-us/azure/storage/blobs/",
    "Cloudinary": "https://cloudinary.com/documentation",
    "Backblaze B2": "https://www.backblaze.com/b2/docs/",
    
    # Messaging providers
    "Firebase Cloud Messaging": "https://firebase.google.com/docs/cloud-messaging",
    "OneSignal": "https://documentation.onesignal.com/docs",
    "Pusher": "https://pusher.com/docs/",
    "PubNub": "https://www.pubnub.com/docs/"
}

@router.get("/api/get_thirdparty")
async def get_thirdparty(
    user_id: Optional[str] = None,
    project_id: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    """
    Mock endpoint for getting third-party API requirements
    
    Query Parameters:
    - user_id: ID of the user (optional)
    - project_id: ID of the project (optional)
    
    Headers:
    - Authorization: Bearer token (automatically sent by frontend)
    
    Returns:
    - Third-party API data based on PRD analysis, or empty object if no APIs needed
    """
    
    # Extract token from Authorization header
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    
    # Log the request
    print(f"\n📡 Get Third-Party APIs Request:")
    print(f"   🔑 Token: {token[:20] + '...' if token else 'None'}")
    print(f"   👤 User ID: {user_id}")
    print(f"   📁 Project ID: {project_id}\n")
    
    # Simulate different responses based on conditions
    # In a real implementation, this would analyze the PRD and determine required APIs
    
    # Example 1: Return empty when no third-party APIs needed
    # return {}
    
    # Example 2: Return list of third-party APIs (generic categories, not specific providers)
    mock_third_party_apis = {
        "apis": [
            {
                "name": "Payment Processing",
                "category": "payment",
                "description": "Secure payment gateway for processing transactions, subscriptions, and refunds",
                "purpose": "Your application requires payment processing capabilities for handling customer transactions, managing subscriptions, and processing refunds securely",
                "providers": PROVIDERS_JSON["payment"]
            },
            {
                "name": "Maps & Location Services",
                "category": "maps",
                "description": "Geolocation and mapping services for address lookup and route planning",
                "purpose": "Based on your PRD, the application needs location-based features including address search, geocoding, distance calculations, and interactive maps",
                "providers": PROVIDERS_JSON["maps"]
            },
            {
                "name": "Authentication & Authorization",
                "category": "oauth",
                "description": "Social login and identity management platform",
                "purpose": "To simplify user onboarding and provide secure authentication, your app needs OAuth integration for social login and SSO capabilities",
                "providers": PROVIDERS_JSON["oauth"]
            },
            {
                "name": "SMS & Messaging",
                "category": "sms",
                "description": "SMS notification and verification services",
                "purpose": "Your application requires SMS capabilities for sending verification codes, transactional alerts, and notifications to users",
                "providers": PROVIDERS_JSON["sms"]
            },
            {
                "name": "Email Services",
                "category": "email",
                "description": "Transactional and marketing email delivery platform",
                "purpose": "For sending user notifications, password resets, promotional emails, and transactional communications reliably at scale",
                "providers": PROVIDERS_JSON["email"]
            },
            {
                "name": "Cloud Storage",
                "category": "storage",
                "description": "Scalable object storage for files and media",
                "purpose": "Your application needs to store and serve user-generated content, images, documents, and media files securely and efficiently",
                "providers": PROVIDERS_JSON["storage"]
            },
            {
                "name": "Push Notifications",
                "category": "messaging",
                "description": "Mobile and web push notification services",
                "purpose": "To engage users with timely updates and alerts, your app requires push notification capabilities across mobile and web platforms",
                "providers": PROVIDERS_JSON["messaging"]
            }
        ],
        "summary": {
            "total": 7,
            "categories": ["payment", "maps", "oauth", "sms", "email", "storage", "messaging"]
        },
        "analyzed_at": datetime.now().isoformat(),
        "prd_version": "1.0.0"
    }
    
    print("   ✅ Returning third-party API requirements")
    
    # To simulate "no third-party APIs needed", uncomment the line below:
    # return {}
    
    return mock_third_party_apis


@router.post("/api/upload_thirdparty")
async def upload_thirdparty(
    request: Dict[str, Any] = Body(...),
    authorization: Optional[str] = Header(None)
):
    """
    Mock endpoint for uploading selected third-party APIs
    
    Accepts:
    - selected_apis: List of selected API objects
    - user_id: ID of the user (optional)
    - project_id: ID of the project (optional)
    
    Headers:
    - Authorization: Bearer token (automatically sent by frontend)
    
    Returns:
    - success: Boolean indicating if upload was successful
    - message: Human-readable message
    - data: Saved APIs data
    """
    
    # Extract fields from request dictionary
    selected_apis = request.get("selected_apis", [])
    user_id = request.get("user_id")
    project_id = request.get("project_id")
    
    # Extract token from Authorization header
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    
    # Log the incoming request for debugging
    print(f"\n📤 Upload Third-Party APIs Request:")
    print(f"   🔑 Token: {token[:20] + '...' if token else 'None'}")
    print(f"   👤 User ID: {user_id}")
    print(f"   📁 Project ID: {project_id}")
    print(f"   🔌 Selected APIs Count: {len(selected_apis)}")
    print(f"   📋 APIs: {[api.get('name', 'Unknown') for api in selected_apis]}\n")
    
    # Accept even if no APIs are selected (user might not need any third-party APIs)
    
    # Enrich selected APIs with providers based on their category
    enriched_apis = []
    for api in selected_apis:
        api_category = api.get("category", "")
        enriched_api = api.copy()
        
        # Add providers for this category if available
        if api_category in PROVIDERS_JSON:
            enriched_api["providers"] = PROVIDERS_JSON[api_category]
        else:
            enriched_api["providers"] = []
        
        enriched_apis.append(enriched_api)
    
    # Mock response data
    response_data = {
        "apis_saved": enriched_apis,
        "count": len(enriched_apis),
        "user_id": user_id,
        "project_id": project_id,
        "saved_at": datetime.now().isoformat(),
        "next_step": "api_factory"
    }
    
    if len(enriched_apis) == 0:
        print("   ℹ️  No third-party APIs selected (proceeding without external APIs)")
        message = "Saved with no third-party APIs"
    else:
        print("   ✅ Third-party APIs saved successfully")
        message = f"Successfully saved {len(enriched_apis)} third-party API(s)"
    
    return {
        "success": True,
        "message": message,
        "data": response_data
    }


@router.post("/api/upload_thirdprovider")
async def upload_thirdprovider(
    request: Dict[str, Any] = Body(...),
    authorization: Optional[str] = Header(None)
):
    """
    Mock endpoint for uploading selected third-party providers
    
    Accepts:
    - selected_providers: Dictionary with category as key and provider name as value
      Example: {"payment": "Stripe", "maps": "Google Maps"}
    - user_id: ID of the user (optional)
    - project_id: ID of the project (optional)
    
    Headers:
    - Authorization: Bearer token (automatically sent by frontend)
    
    Returns:
    - success: Boolean indicating if upload was successful
    - message: Human-readable message
    - data: Saved providers data with API key requirements
    """
    
    # Extract fields from request dictionary
    selected_providers = request.get("selected_providers", {})
    user_id = request.get("user_id")
    project_id = request.get("project_id")
    
    # Extract token from Authorization header
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    
    # Log the incoming request for debugging
    print(f"\n📤 Upload Third-Party Providers Request:")
    print(f"   🔑 Token: {token[:20] + '...' if token else 'None'}")
    print(f"   👤 User ID: {user_id}")
    print(f"   📁 Project ID: {project_id}")
    print(f"   🔌 Selected Providers Count: {len(selected_providers)}")
    print(f"   📋 Providers: {selected_providers}\n")
    
    # Validate that at least one provider is selected
    if not selected_providers or len(selected_providers) == 0:
        raise HTTPException(
            status_code=400,
            detail="At least one provider must be selected"
        )
    
    # Generate API key requirements for each selected provider
    api_key_requirements = []
    for category, provider_name in selected_providers.items():
        # Define what keys each provider needs
        key_info = {
            "category": category,
            "provider": provider_name,
            "keys_required": []
        }
        
        # Provider-specific key requirements
        if provider_name == "Stripe":
            key_info["keys_required"] = [
                {"name": "Publishable Key", "field": "stripe_publishable_key", "description": "Public key for client-side", "required": True},
                {"name": "Secret Key", "field": "stripe_secret_key", "description": "Secret key for server-side", "required": True}
            ]
        elif provider_name == "PayPal":
            key_info["keys_required"] = [
                {"name": "Client ID", "field": "paypal_client_id", "description": "PayPal application client ID", "required": True},
                {"name": "Client Secret", "field": "paypal_client_secret", "description": "PayPal application secret", "required": True}
            ]
        elif provider_name == "Google Maps":
            key_info["keys_required"] = [
                {"name": "API Key", "field": "google_maps_api_key", "description": "Google Maps API key", "required": True}
            ]
        elif provider_name == "Mapbox":
            key_info["keys_required"] = [
                {"name": "Access Token", "field": "mapbox_access_token", "description": "Mapbox public access token", "required": True}
            ]
        elif provider_name == "Auth0":
            key_info["keys_required"] = [
                {"name": "Domain", "field": "auth0_domain", "description": "Auth0 tenant domain", "required": True},
                {"name": "Client ID", "field": "auth0_client_id", "description": "Application client ID", "required": True},
                {"name": "Client Secret", "field": "auth0_client_secret", "description": "Application client secret", "required": True}
            ]
        elif provider_name == "Firebase Auth":
            key_info["keys_required"] = [
                {"name": "API Key", "field": "firebase_api_key", "description": "Firebase API key", "required": True},
                {"name": "Project ID", "field": "firebase_project_id", "description": "Firebase project ID", "required": True}
            ]
        elif provider_name == "Twilio":
            key_info["keys_required"] = [
                {"name": "Account SID", "field": "twilio_account_sid", "description": "Twilio account SID", "required": True},
                {"name": "Auth Token", "field": "twilio_auth_token", "description": "Twilio auth token", "required": True}
            ]
        elif provider_name == "SendGrid":
            key_info["keys_required"] = [
                {"name": "API Key", "field": "sendgrid_api_key", "description": "SendGrid API key", "required": True}
            ]
        elif provider_name == "AWS S3":
            key_info["keys_required"] = [
                {"name": "Access Key ID", "field": "aws_access_key_id", "description": "AWS access key ID", "required": True},
                {"name": "Secret Access Key", "field": "aws_secret_access_key", "description": "AWS secret access key", "required": True},
                {"name": "Region", "field": "aws_region", "description": "AWS region (e.g., us-east-1)", "required": True},
                {"name": "Bucket Name", "field": "aws_bucket_name", "description": "S3 bucket name", "required": True}
            ]
        else:
            # Generic API key for other providers
            key_info["keys_required"] = [
                {"name": "API Key", "field": f"{category}_api_key", "description": f"{provider_name} API key", "required": True}
            ]
        
        api_key_requirements.append(key_info)
    
    # Mock response data
    response_data = {
        "providers_saved": selected_providers,
        "count": len(selected_providers),
        "api_key_requirements": api_key_requirements,
        "user_id": user_id,
        "project_id": project_id,
        "saved_at": datetime.now().isoformat(),
        "next_step": "enter_api_keys"
    }
    
    print("   ✅ Third-party providers saved successfully")
    print(f"   🔑 API keys required: {len(api_key_requirements)}")
    
    return {
        "success": True,
        "message": f"Successfully saved {len(selected_providers)} provider(s)",
        "data": response_data
    }