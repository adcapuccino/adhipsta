'use strict';

angular.module('adcappuccinoApp')
  .factory('User', function ($resource) {
    return $resource('/api/users/:id/:controller', {
      id: '@_id'
    },
    {
      changePassword: {
        method: 'PUT',
        params: {
          controller:'password'
        }
      },
      releaseApiToken: {
        url: '/auth/adwords/api_token',
        method: 'DELETE',
      },
      get: {
        url: '/api/users/me',
        method: 'GET'
      }
	  });
  });
