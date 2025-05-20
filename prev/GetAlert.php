<?php 
    //https://youtu.be/GmR4-AiJjPE 이 영상을 참고하세요!
    header("Content-Type: application/json; charset=utf-8");


    $data =file_get_contents('php://input');

    #$data = '{"dist":"upbit","ticker":"KRW-BTC","type":"market","side":"sell","price_money":5000,"amt":0.001,"etc_num":0.3,"etc_str":"122121"}';

    $command = "python3 /var/autobot/GetWebhook.py ". escapeshellarg($data);
    exec($command, $output, $return_var);
    $json_array = json_encode($output);
    echo $json_array

?>
