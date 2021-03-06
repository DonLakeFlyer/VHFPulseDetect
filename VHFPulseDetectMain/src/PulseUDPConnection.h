#pragma once

#include <string>
#include <mutex>
#include <thread>
#include <atomic>
#include <vector>
#include <cstdint>

class PulseUDPConnection  {
public:
    explicit PulseUDPConnection(const std::string& local_ip, int local_port);
    ~PulseUDPConnection();

    bool start();
    void stop();

    // Non-copyable
    PulseUDPConnection(const PulseUDPConnection&) = delete;
    const PulseUDPConnection& operator=(const PulseUDPConnection&) = delete;

private:
    bool setup_port();
    void start_recv_thread();

    void receive();

    std::string _local_ip;
    int _local_port_number;

    std::mutex _remote_mutex{};
    struct Remote {
        std::string ip{};
        int port_number{0};

        bool operator==(const PulseUDPConnection::Remote& other)
        {
            return ip == other.ip && port_number == other.port_number;
        }
    };
    std::vector<Remote> _remotes{};

    int _socket_fd{-1};
    std::thread* _recv_thread{nullptr};
    std::atomic_bool _should_exit{false};
};
