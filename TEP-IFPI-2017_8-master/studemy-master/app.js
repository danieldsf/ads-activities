Lockr.prefix = 'lckr';

const app = angular.module('myApp', ['ngRoute']).run(function($rootScope, $http, $location) {    
    $rootScope.user = function(){
        return Lockr.get('user');
    }

    $rootScope.getMySelf = function(){
        $http.get($rootScope.API + 'get-myself/', {}).then((response) => {
            let retorno = response.data;
            Lockr.set('user', retorno);   
            window.location.reload();
        }).catch((error) => {
            $rootScope.showMessage('Erro!', 'Erro ao carregar dados');
        });
    }

    $rootScope.API = 'http://localhost:8000/api/';

    $rootScope.isLogged = function(){
        $rootScope.setToken(Lockr.get('token', null));
    }

    $rootScope.getType = function(){
        return $rootScope.getUser() === 'TE' ? 'Professor' : 'Aluno';
    }

    $rootScope.showMessage = function(title, body){
        $.alert({
            title: title,
            content: body,
        });
    }

    $rootScope.setToken = function(token) {
        
        if(!token && (!Lockr.get('token', false) || (Lockr.get('token') == 'null'))) {
            delete $http.defaults.headers.common.Authorization;
            Lockr.rm('token');
            window.location = "#!/login";
            Lockr.flush();      
        } else {
            Lockr.set('token', token);
            $http.defaults.headers.common.Authorization = 'Token ' + Lockr.get('token');
        }
    }

    $rootScope.logout = function(){
        $rootScope.setToken(null);
        
        Lockr.flush();

        window.location = "#!/login";
    }

    $rootScope.getUser = function(){
        if(Lockr.get('user', false)){
            return Lockr.get('user')
        }else{
            $rootScope.setToken(null);
            window.location = "#!/login";
            return null;
        }
    }
});

app.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl : "src/courses/all.htm",
        controller: "AllCoursesPCtrl"
    })
    .when("/dashboard", {
        templateUrl : "src/dashboard.html",
        controller: "DashboardCtrl"
    })
    .when("/login", {
        templateUrl : "src/login.htm",
        controller: "MainCtrl"
    })
    .when("/courses", {
        templateUrl : "src/courses/all.htm",
        controller: "AllCoursesCtrl"
    })
    .when("/all-courses", {
        templateUrl : "src/courses/all_private.htm",
        controller: "AllCoursesCtrl"
    })
    .when("/faturamento", {
        templateUrl : "src/courses/faturamento.html",
        controller: "FaturamentoCtrl"
    })
    .when("/recover", {
        templateUrl : "src/courses/recover.htm",
        controller: "RecoverCtrl"
    })
    .otherwise({
        template : "<h1>Página não encontrada, clique no botão de voltar</h1>"
    });
});

app.controller('AllCoursesPCtrl', function($scope, $http) {
    $scope.cursos = [];

    $scope.list = function(){
        axios.get($scope.API + 'courses/')
        .then(function (response) {
            $scope.cursos = response.data;
            $scope.$apply();
        })
        .catch(function(error){
            
        });
    }

    $scope.list();
});

app.controller('MainCtrl', function($scope, $http) {
    $scope.username = '';
    $scope.password = '';

    $scope.login = function(){
        $http.post($scope.API + 'token-auth/', {
            username: $scope.username,
            password: $scope.password
        }).then((response) => {
            $scope.showMessage('Sucesso!', 'Login Correto');
            let retorno = response.data;
            if(retorno.token !== undefined){ 
                $scope.setToken(retorno.token);
                Lockr.set('user_id', retorno.user_id);
                Lockr.set('user', retorno.user);   
                window.location = '#!/dashboard';
            }            
        }).catch((error) => {
            $scope.showMessage('Erro!', 'Login Inválido');
        });
    }

    $scope.createAccount = function(){

    }

    $scope.sendEmail = function(email){
        $http.post($scope.API + 'reset-password', {email: email}).then(function(response){

        }, function(error){
            $scope.showMessage('Erro');
        });
    }

    $scope.resetAccount = function(){
        $scope.email = '';

        $.confirm({
            title: 'Prompt!',
            content: '' +
            '<form action="" class="formName">' +
            '<div class="form-group">' +
            '<label>Enter something here</label>' +
            '<input type="text" placeholder="Your name" class="name form-control" required />' +
            '</div>' +
            '</form>',
            buttons: {
                formSubmit: {
                    text: 'Submit',
                    btnClass: 'btn-blue',
                    action: function () {
                        var name = this.$content.find('.name').val();
                        if(!name){
                            $.alert('Digite um e-mail válido');
                            return false;
                        }
                        //$scope.email = name;

                        $scope.sendEmail(name);
                    }
                },
                cancel: function () {
                    //close
                },
            },
            onContentReady: function () {
                // bind to events
                var jc = this;
                this.$content.find('form').on('submit', function (e) {
                    // if the user submits the form by pressing enter in the field.
                    e.preventDefault();
                    jc.$$formSubmit.trigger('click'); // reference the button and click it
                });
            }
        });
    }
});

app.controller('DashboardCtrl', function($scope, $http) {
    $scope.isLogged();

    $scope.refresh = function(){
        $scope.getMySelf();
    }

    $scope.favorite = function(id){
        $http.post($scope.API + 'favorite-course/', {
            course: id
        }).then((response) => {
            $scope.showMessage('Sucesso!', 'Curso Favoritado, Aguardando Aprovação');
            $scope.getMySelf();
        }).catch((error) => {
            $scope.showMessage('Erro!', 'Login Inválido');
        });
    }

    $scope.remove = function(id){
        $http.post($scope.API + 'remove-course/', {
            course: id
        }).then((response) => {
            $scope.showMessage('Sucesso!', 'Curso Comprado, Aguardando Aprovação');
            
            let retorno = response.data;

            $scope.getMySelf();          
        }).catch((error) => {
            $scope.showMessage('Erro!', 'Login Inválido');
        });
    }

    $scope.cursos = [];
    
    $scope.curso = {
        name: '',
        price: 0
    };
    
    $scope.user = $scope.getUser();

    $scope.list = function(){
        $http.get($scope.API + 'created-courses/')
        .then(function (response) {$scope.cursos = response.data}, function(error){
            window.location = '#!/login';
        });
    }

    $scope.list();

    $scope.save = function(){
        if($scope.curso.id){
            $scope.update();
            return; 
        }

        $http.post($scope.API + 'created-courses/', $scope.curso).then(function (response){
            $scope.showMessage('Sucesso!', 'Curso cadastrado');
            $scope.list();
            $('.modal').modal('hide');
        }, function (error) {
            if(error.headers.status == 401){
                $scope.setToken(null);
            }else{
                $scope.showMessage('Erro!', error.data.detail)
            }
        });
    }

    $scope.select = function(id){
        $scope.curso = $scope.cursos.filter(x => x.id == id)[0];
        console.log($scope.curso);
    }

    $scope.add = function(){
        $scope.curso = {
            name: '',
            price: 0
        };
    }

    $scope.delete = function(id){
        $http.delete($scope.API + 'created-courses/' + id + '/', $scope.curso).then(function (response){
            $scope.showMessage('Sucesso!', 'Curso deletado');
            $scope.list();
        }, function (error) {
            if(error.headers.status == 401){
                $scope.setToken(null);
            }else{
                $scope.showMessage('Erro!', 'Erro na deleção');
            }
        });
    }

    $scope.update = function(){
        $http.put($scope.API + 'created-courses/' + $scope.curso.id+ '/', $scope.curso).then(function (response){
            $scope.showMessage('Sucesso!', 'Curso editado');
            $scope.list();
            $scope.curso = {};
        }, function (error) {
            if(error.headers.status == 401){
                $scope.setToken(null);
            }else{
                $scope.showMessage('Erro!', 'Erro na atualiação');
            }
        });
    }
});

app.controller('AllCoursesCtrl', function($scope, $http) {
    $scope.isLogged();

    $scope.cursos = [];
    $scope.curso = {};

    $scope.list = function(){
        $http.get($scope.API + 'courses/')
        .then(function (response) {$scope.cursos = response.data}, function(error){
            window.location = '#!/login';
        });
    }

    $scope.buy = function(id){
        $http.post($scope.API + 'buy-course/', {
            course: id
        }).then((response) => {
            $scope.showMessage('Sucesso!', 'Curso Comprado, Aguardando Aprovação');
            
            let retorno = response.data;

            if(retorno.token !== undefined){ 
                $scope.setToken(retorno.token);
                Lockr.set('user_id', retorno.user_id);
                Lockr.set('user', retorno.user);   
                window.location = '#!/dashboard';
            }            
        }).catch((error) => {
            $scope.showMessage('Erro!', 'Login Inválido');
        });
    }

    $scope.list();
});

app.controller('FaturamentoCtrl', function($scope, $http) {
    $scope.isLogged();
    $scope.faturamento = 0;

    $scope.getFaturamento = function(){
        $http.get($scope.API + 'get-faturamento/')
        .then(function (response) {$scope.faturamento = response.data.faturamento}, function(error){
            window.location = '#!/login';
        });
    }
    
    $scope.getFaturamento();

});

app.controller('RecoverCtrl', function($scope, $http) {
    $scope.email = '';

    $scope.recover = function(){
        axios.post($scope.API + 'password-reset/reset_password/', {'email': $scope.email})
        .then(function (response) {
            $scope.showMessage('Sucesso', 'Email enviado para voce!');
            $scope.$apply();
        })
        .catch(function(error){
            //window.location = '#!/login';
        });
    }

});

