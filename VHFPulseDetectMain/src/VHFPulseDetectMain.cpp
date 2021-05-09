//
// Simple example to demonstrate how to use the MAVSDK.
//

#include <chrono>
#include <cstdint>
#include <mavsdk/mavsdk.h>
#include <mavsdk/plugins/action/action.h>
#include <mavsdk/plugins/telemetry/telemetry.h>
#include <iostream>
#include <thread>

#include "PulseUDPConnection.h"

using namespace mavsdk;
using namespace std::this_thread;
using namespace std::chrono;

#define ERROR_CONSOLE_TEXT "\033[31m" // Turn text on console red
#define TELEMETRY_CONSOLE_TEXT "\033[34m" // Turn text on console blue
#define NORMAL_CONSOLE_TEXT "\033[0m" // Restore normal console colour

void usage(std::string bin_name)
{
    std::cout << NORMAL_CONSOLE_TEXT << "Usage : " << bin_name << " <connection_url>" << std::endl
              << "Connection URL format should be :" << std::endl
              << " For TCP : tcp://[server_host][:server_port]" << std::endl
              << " For UDP : udp://[bind_host][:bind_port]" << std::endl
              << " For Serial : serial:///path/to/serial/dev[:baudrate]" << std::endl
              << "For example, to connect to the simulator use URL: udp://:14540" << std::endl;
}

void component_discovered(ComponentType component_type)
{
    std::cout << NORMAL_CONSOLE_TEXT << "Discovered a component with type "
              << unsigned(component_type) << std::endl;
}

int main(int argc, char** argv)
{
    PulseUDPConnection pulseUDP("127.0.0.1", 10000);
    if (!pulseUDP.start()) {
        std::cout << ERROR_CONSOLE_TEXT << "PulseUDPConnection.start failed"
                  << NORMAL_CONSOLE_TEXT << std::endl;
        return 1;      
    }

    Mavsdk mavsdk;
    mavsdk.set_configuration(Mavsdk::Configuration(Mavsdk::Configuration::UsageType::CompanionComputer));

    //std::string connection_url;
    //ConnectionResult connection_result;

    //bool discovered_system = false;
    if (argc == 2) {
#if 0
        connection_url = argv[1];
        connection_result = mavsdk.add_any_connection(connection_url);
#endif
    } else {
        usage(argv[0]);
        return 1;
    }

#if 0
    if (connection_result != ConnectionResult::Success) {
        std::cout << ERROR_CONSOLE_TEXT << "Connection failed: " << connection_result
                  << NORMAL_CONSOLE_TEXT << std::endl;
        return 1;
    }

    std::cout << "Waiting to discover system..." << std::endl;
    mavsdk.subscribe_on_new_system([&mavsdk, &discovered_system]() {
        const auto system = mavsdk.systems().at(0);

        if (system->is_connected()) {
            std::cout << "Discovered system" << std::endl;
            discovered_system = true;
        }
    });

    // We usually receive heartbeats at 1Hz, therefore we should find a system after around 2
    // seconds.
    sleep_for(seconds(20));

    if (!discovered_system) {
        std::cout << ERROR_CONSOLE_TEXT << "No system found, exiting." << NORMAL_CONSOLE_TEXT
                  << std::endl;
        return 1;
    }

    const auto system = mavsdk.systems().at(0);


    // Register a callback so we get told when components (camera, gimbal) etc
    // are found.
    system->register_component_discovered_callback(component_discovered);

    auto telemetry = Telemetry{system};
    auto action = Action{system};

    // We want to listen to the altitude of the drone at 1 Hz.
    Telemetry::Result set_rate_result = telemetry.set_rate_position(1.0);
    if (set_rate_result != Telemetry::Result::Success) {
        std::cout << ERROR_CONSOLE_TEXT << "Setting altitude rate failed:" << set_rate_result
                  << NORMAL_CONSOLE_TEXT << std::endl;
        return 1;
    }

    // Set up callback to monitor position
    telemetry.subscribe_position([](Telemetry::Position position) {
        std::cout << TELEMETRY_CONSOLE_TEXT // set to blue
                  << "Altitude: " << position.relative_altitude_m << " m"
                  << NORMAL_CONSOLE_TEXT // set to default color again
                  << std::endl;
    });

    // We want to listen to the gps of the drone at 1 Hz.
    set_rate_result = telemetry.set_rate_gps_info(1.0);
    if (set_rate_result != Telemetry::Result::Success) {
        std::cout << ERROR_CONSOLE_TEXT << "Setting gps rate failed:" << set_rate_result
                  << NORMAL_CONSOLE_TEXT << std::endl;
        return 1;
    }

    // Set up callback to monitor gps
    telemetry.subscribe_gps_info([](Telemetry::GpsInfo gps_info) {
        std::cout << TELEMETRY_CONSOLE_TEXT // set to blue
                  << "GPS, num satellites: " << gps_info.num_satellites << ", "
                  << "fix type: " << gps_info.fix_type
                  << NORMAL_CONSOLE_TEXT // set to default color again
                  << std::endl;
    });

    // We want to listen to the battery of the drone at 1 Hz.
    set_rate_result = telemetry.set_rate_battery(1.0);
    if (set_rate_result != Telemetry::Result::Success) {
        std::cout << ERROR_CONSOLE_TEXT << "Setting battery rate failed:" << set_rate_result
                  << NORMAL_CONSOLE_TEXT << std::endl;
        return 1;
    }

    // Set up callback to monitor battery
    telemetry.subscribe_battery([](Telemetry::Battery battery) {
        std::cout << TELEMETRY_CONSOLE_TEXT // set to blue
                  << "Battery: " << battery.voltage_v << " v,"
                  << "remaining: " << int(battery.remaining_percent * 1e2f) << " %"
                  << NORMAL_CONSOLE_TEXT // set to default color again
                  << std::endl;
    });
#endif

    while(true) {
        sleep_for(seconds(10));
    }
    return 0;
}
