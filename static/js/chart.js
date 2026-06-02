document.addEventListener("DOMContentLoaded", () => {
    const chartCanvas = document.getElementById('progressChart');
    if (!chartCanvas) return; 

    fetch('/api/chart-data')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data.labels || data.labels.length === 0) {
                const container = chartCanvas.parentNode;
                container.innerHTML = `
                    <div class="flex flex-col items-center justify-center h-full py-12 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 text-center">
                        <span class="text-4xl mb-3">📊</span>
                        <p class="text-gray-700 font-semibold text-sm">Chưa có dữ liệu tiến trình học tập</p>
                        <p class="text-gray-400 text-xs mt-1 px-4">Hãy hoàn thành tối thiểu một bài luyện nghe để kích hoạt hệ thống phân tích đồ thị hiệu suất.</p>
                    </div>`;
                return;
            }

            const ctx = chartCanvas.getContext('2d');
            
            const gradientScore = ctx.createLinearGradient(0, 0, 0, 300);
            gradientScore.addColorStop(0, 'rgba(59, 130, 246, 0.4)'); 
            gradientScore.addColorStop(1, 'rgba(59, 130, 246, 0.0)'); 

            const gradientAccuracy = ctx.createLinearGradient(0, 0, 0, 300);
            gradientAccuracy.addColorStop(0, 'rgba(16, 185, 129, 0.15)'); 
            gradientAccuracy.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels, // Mốc thời gian (X-Axis)
                    datasets: [
                        {
                            label: 'Điểm tổng kết (Thời gian + Văn bản)',
                            data: data.scores,
                            borderColor: '#3b82f6', // Tailwind Blue-500
                            backgroundColor: gradientScore,
                            borderWidth: 3,
                            fill: true,             // Kích hoạt đổ vùng màu phía dưới đường line
                            tension: 0.3,           // Bo cong đường nối giữa các điểm (Cubic spline interpolation)
                            pointBackgroundColor: '#3b82f6',
                            pointHoverRadius: 7,    // Phóng to điểm khi di chuột vào
                            pointRadius: 4
                        },
                        {
                            label: 'Độ chính xác chuỗi ký tự (%)',
                            data: data.accuracies,
                            borderColor: '#10b981', // Tailwind Green-500
                            backgroundColor: gradientAccuracy,
                            borderWidth: 2,
                            borderDash: [5, 5],     // Định dạng đường nét đứt để phân biệt trực quan
                            fill: true,
                            tension: 0.3,
                            pointBackgroundColor: '#10b981',
                            pointHoverRadius: 6,
                            pointRadius: 3
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false, // Cho phép biểu đồ co giãn linh hoạt theo thẻ bao ngoài
                    interaction: {
                        mode: 'index',          // Khi hover, hiển thị giá trị của cả 2 đường tại cùng một trục X
                        intersect: false
                    },
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                boxWidth: 15,
                                font: { family: 'Inter, sans-serif', size: 12, weight: '500' },
                                color: '#4b5563' // Gray-600
                            }
                        },
                        tooltip: {
                            backgroundColor: '#1f2937', // Thao tác tùy chỉnh Theme tối (Gray-800) cho Tooltip
                            titleFont: { size: 13, weight: 'bold', family: 'Inter' },
                            bodyFont: { size: 12, family: 'Inter' },
                            padding: 12,
                            borderRadius: 8,
                            shadowBlur: 4,
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) label += ': ';
                                    if (context.parsed.y !== null) label += context.parsed.y.toFixed(1);
                                    return label;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            min: 0,
                            max: 100,
                            ticks: {
                                color: '#9ca3af', // Gray-400
                                stepSize: 20
                            },
                            grid: {
                                color: '#f3f4f6' // Đường lưới mờ tinh tế (Gray-100)
                            },
                            title: {
                                display: true,
                                text: 'Thang hiệu suất (0 - 100)',
                                color: '#6b7280',
                                font: { weight: '600', size: 11 }
                            }
                        },
                        x: {
                            ticks: {
                                color: '#9ca3af',
                                maxRotation: 30,
                                minRotation: 30
                            },
                            grid: {
                                display: false // Tắt grid dọc để biểu đồ thông thoáng hơn
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Lỗi trong tiến trình nạp dữ liệu đồ thị:', error);
            chartCanvas.parentNode.innerHTML = `
                <div class="text-center py-8 text-red-500 bg-red-50 rounded-2xl border border-red-200 text-xs">
                    ⚠️ Không thể tải dữ liệu biểu đồ. Vui lòng kiểm tra lại kết nối Backend.
                </div>`;
        });
});
  