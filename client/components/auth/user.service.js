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
        method: 'DELETE',
        params: {
          id: 'me',
          controller:'api_token'
        }
      },
      get: {
        method: 'GET',
        params: {
          id:'me'
        }
      }
	  });
  });
