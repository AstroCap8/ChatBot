<?php

    $dbn = new PDO('sqlite:tasks.sqlite');

    $query = "SELECT * FROM tasks";

    $task_info = [
        "id" => 0,
        "fullname" => 'unknown',
        "task" => 'unknown',
        "status" => 'unknown',
        "categorie" => 'unknown'
    ];

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./css/bootstrap.css">
    <link rel="stylesheet" href="./css/styles.css">
    <title>Главная</title>
</head>
<body>

    <div class="container-fluid whiteb">    
        <div class="row whiteb">
            <div class="col-lg-12 p-2 fs-4 text-center">Панель администратора</div>
        </div>
    </div>
    <div class="container-fluid">   
        <div class="row taskblock">
                <div class="col-lg-8">
                    <div class="row">
                        <div class="col-lg-12">
                            <h2>Текущие задачи</h2>
                        </div>

            <?php
            
            foreach ($dbn->query($query) as $row)
            {

            if($row['status'] != 'Выполнена'){

            echo 
            '
                        <div class="col-lg-8 pt-4 pb-2 podtaskblock">
                            <p class="fs-4"> <strong>Пользователь: </strong>' . ($row['fullname']) . '<br> <strong>Должность: </strong>' . ($row['chin']) .'<br> <strong>Статус: </strong> ' . ($row['status']) . '<br> <strong>Задача: </strong>' . ($row['task']) . '</p> 
                        </div> 
                        <div class="col-lg-2 pt-4 pb-2 podtaskblock">
                        <a href="">
                            <div class="fs-5 pb-2 mb-1 text-center tbutton">
                                    Выполнить задачу
                            </div>
                        </a>
                        <a href="фыв">
                            <div class="fs-5 pb-2 mb-1 text-center tbutton">
                                Удалить задачу
                            </div>
                            </a>
                        </div>
            ';
                        }
            }
            ?>
                    </div>
                </div>
            
                <div class="col-lg-4">
                    <div class="row">
                        <div class="col-lg-12">
                            <h2>Выполненные задачи</h2>
                        </div>
                        <?php
            
                        foreach ($dbn->query($query) as $row)
                        {
                        
                        if($row['status'] == 'Выполнена'){

                        echo 
                        '
                                    <div class="col-lg-12 pt-4 pb-2 podtaskblock">
                                        <p class="fs-4"> <strong>Пользователь: </strong>' . ($row['fullname']) . '<br> <strong>Должность: </strong>' . ($row['chin']) . '<br> <strong>Статус: </strong> ' . ($row['status']) . '<br> <strong>Задача: </strong>' . ($row['task']) . '</p> </div> ';
                        }
                    }

                        ?>
                    </div>
                </div>
        </div>
    </div>

    <script src="./js/bootstrap.js"></script>
</body>
</html>

<?php

    $dbn = null;

?>