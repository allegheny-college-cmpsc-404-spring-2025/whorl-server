"""
Django Middleware Components for Authentication and Logging.

This module provides two middleware components:

1. GitHub Authentication: Authenticates incoming requests using GitHub tokens.
    It validates that the provided token belongs to the user making the request
    by comparing the GitHub username from the token with the username provided
    in the request headers.

2. Request Logging: Logs successful HTTP requests (status codes 200-399) to help
    with monitoring and debugging application behavior.

Together, these middlewares enhance the security and observability of the application.
"""

import requests
import logging
from django.http import JsonResponse


class GitHubTokenAuthenticationMiddleware:
    """
    Middleware to authenticate requests using a GitHub token.
    
    This middleware intercepts incoming requests and validates the GitHub
    authentication token provided in the HTTP_AUTHORIZATION header against
    the GitHub API. It ensures that the token is valid and belongs to the
    user specified in the HTTP_USER header.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the given response handler.
        
        Args:
            get_response: The next middleware or view in the Django request/response chain
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the incoming request and authenticate the GitHub token.
        
        This method extracts the GitHub token from the request headers,
        validates it against the GitHub API, and ensures the token belongs
        to the specified user. If authentication succeeds, the request is
        passed to the next handler; otherwise, a 403 Forbidden response is returned.
        
        Args:
            request: The Django HttpRequest object
            
        Returns:
            HttpResponse: Either the response from the next handler if authentication
            succeeds, or a 403 Forbidden JsonResponse if it fails
        """
        headers = request.META
        token = headers.get("HTTP_AUTHORIZATION")
        http_user = headers.get("HTTP_USER")

        headers = {
            "Authorization": f"{token}",
        }

        # Fetch the authenticated user's details
        user_response = requests.get("https://api.github.com/user", headers=headers)
        if user_response.status_code == 200:
            user_data = user_response.json()
            if user_data.get("login") == http_user:
                # User is authenticated
                response = self.get_response(request)
                return response
            else:
                # User is not authenticated
                return JsonResponse({"detail": "Forbidden"}, status=403)
        else:
            return JsonResponse({"detail": "Forbidden"}, status=403)

class RequestLoggingMiddleware:
    """
    Middleware to log successful HTTP requests.
    
    This middleware intercepts responses and logs information about successful 
    HTTP requests (status codes 200-399) to help with monitoring and debugging
    application behavior.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the given response handler.
        
        Args:
            get_response: The next middleware or view in the Django request/response chain
        """
        self.get_response = get_response
        self.logger = logging.getLogger('django.request')

    def __call__(self, request):
        """
        Process the request and log successful responses.
        
        This method passes the request to the next handler and logs information
        about successful responses (status codes 200-399) to the request logger.
        
        Args:
            request: The Django HttpRequest object
            
        Returns:
            HttpResponse: The response from the next handler in the middleware chain
        """
        response = self.get_response(request)
        
        if 200 <= response.status_code < 400:
            self.logger.info("sucess request")

        return response