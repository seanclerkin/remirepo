<?php
$vendorDir = '/usr/share/php';
// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefixes(array(
    'Seld\\JsonLint\\'             => $vendorDir,
    'Seld\\PharUtils\\'            => $vendorDir,
    'Seld\\CliPrompt\\'            => $vendorDir,
    'Symfony\\Component\\'         => $vendorDir,
    'Composer\\'                   => dirname(__DIR__)
));
$fedoraClassLoader->register();

// Dependencies
require_once $vendorDir . '/Composer/Spdx/autoload.php';
require_once $vendorDir . '/Composer/Semver/autoload.php';
require_once $vendorDir . '/JsonSchema/autoload.php';
