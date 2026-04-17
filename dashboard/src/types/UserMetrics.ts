interface User {
  id: number;
  tg_id: string;
  full_name: string;
  is_blacklisted: boolean;
}

interface HealthMetric {
  id: number;
  metric: string;
  user_tg_id: string;
  value: number;
  date: string | Date;
}

interface UserMetrics {
  user: User;
  metrics: HealthMetric[];
}

export default UserMetrics;