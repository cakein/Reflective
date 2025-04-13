<?php
header('Content-Type: text/plain');
$feedbackDir = 'output/feedback/';
$output = [];

if (is_dir($feedbackDir)) {
    $files = glob($feedbackDir . '/*.log');
    foreach ($files as $file) {
        $content = file_get_contents($file);
        if ($content !== false) {
            $filename = basename($file, '.log');
            $output[] = $filename . ': ' . trim($content);
        }
    }
}

echo implode("\n", $output);
?>
