'use strict';

angular.module('adhipstaApp')
  .controller('CampaignsCtrl', function ($scope, $http) {
      $scope.message = 'Loading...';
      $scope.error = '';
      $http.get('/api/adwords/campaigns').success(function(data) {
          $scope.campaigns = data;
          $scope.message = '';
      }).error(function(data) {
          $scope.message = '';
          $scope.error = data;
      });
  });