'use strict';

angular.module('adhipstaApp')
  .controller('SettingsCtrl', function ($scope, $window, User, Auth) {
    $scope.errors = {};

    $scope.changePassword = function(form) {
      $scope.submitted = true;
      if(form.$valid) {
        Auth.changePassword( $scope.user.oldPassword, $scope.user.newPassword )
        .then( function() {
          $scope.message = 'Password successfully changed.';
        })
        .catch( function() {
          form.password.$setValidity('mongoose', false);
          $scope.errors.other = 'Incorrect password';
          $scope.message = '';
        });
      }
    };
    
    $scope.user = Auth.getCurrentUser();

    $scope.obtainApiToken = function() {
      $window.location.href = '/auth/adwords';  
    };
    
    $scope.releaseApiToken = function() {
      User.releaseApiToken().$promise.then(function() {
          $scope.user.has_api_token = false;
      })
      .catch(function() {
          $scope.errors.other = 'Failed to remove token';
      });
    };
  });
