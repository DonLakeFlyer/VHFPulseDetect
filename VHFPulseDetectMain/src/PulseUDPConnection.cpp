#include "PulseUDPConnection.h"

#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>
#include <unistd.h> // for close()
#include <iostream>
#include <string.h>

#include <cassert>
#include <algorithm>

#define GET_ERROR(_x) strerror(_x)

PulseUDPConnection::PulseUDPConnection(const std::string& local_ip,int local_port_number)
    : _local_ip         (local_ip)
    , _local_port_number(local_port_number)
{

}

PulseUDPConnection::~PulseUDPConnection()
{
    // If no one explicitly called stop before, we should at least do it.
    stop();
}

bool PulseUDPConnection::start()
{
    if (!setup_port()) {
        return false;
    }

    start_recv_thread();

    return true;
}

bool PulseUDPConnection::setup_port()
{
    _socket_fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    if (_socket_fd < 0) {
        std::cout << "socket error" << GET_ERROR(errno) << std::endl;
        return false;
    }

    struct sockaddr_in addr {};
    addr.sin_family = AF_INET;
    inet_pton(AF_INET, _local_ip.c_str(), &(addr.sin_addr));
    addr.sin_port = htons(_local_port_number);

    if (bind(_socket_fd, reinterpret_cast<sockaddr*>(&addr), sizeof(addr)) != 0) {
        std::cout << "bind error: " << GET_ERROR(errno) << std::endl;
        return false;
    }

    return true;
}

void PulseUDPConnection::start_recv_thread()
{
    _recv_thread = new std::thread(&PulseUDPConnection::receive, this);
}

void PulseUDPConnection::stop()
{
    _should_exit = true;

    // This should interrupt a recv/recvfrom call.
    shutdown(_socket_fd, SHUT_RDWR);

    // But on Mac, closing is also needed to stop blocking recv/recvfrom.
    close(_socket_fd);

    if (_recv_thread) {
        _recv_thread->join();
        delete _recv_thread;
        _recv_thread = nullptr;
    }
}

void PulseUDPConnection::receive()
{
    std::cout << "PulseUDPConnection::receive" << std::endl;

    // Enough for MTU 1500 bytes.
    char buffer[sizeof(int) + sizeof(float)];

    while (!_should_exit) {
        struct sockaddr_in src_addr = {};
        socklen_t src_addr_len = sizeof(src_addr);
        const auto recv_len = recvfrom(
            _socket_fd,
            buffer,
            sizeof(buffer),
            0,
            reinterpret_cast<struct sockaddr*>(&src_addr),
            &src_addr_len);

        if (recv_len == 0) {
            // This can happen when shutdown is called on the socket,
            // therefore we check _should_exit again.
            continue;
        }

        if (recv_len < 0) {
            // This happens on destruction when close(_socket_fd) is called,
            // therefore be quiet.
            // std::cout << "recvfrom error: " << GET_ERROR(errno);
            continue;
        }

        std::cout << "Pulse " << *((int *)&buffer[0]) << " " << *((float *)&buffer[sizeof(int)]) << std::endl;
    }
}
