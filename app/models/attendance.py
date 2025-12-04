"""
打卡记录模型
"""
from app import db
from datetime import datetime, date, time


class AttendanceRecord(db.Model):
    """打卡记录表"""
    __tablename__ = 'attendance_records'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    attendance_date = db.Column(db.Date, nullable=False, default=date.today, comment='打卡日期')
    check_in_time = db.Column(db.DateTime, comment='上班打卡时间')
    check_out_time = db.Column(db.DateTime, comment='下班打卡时间')
    work_hours = db.Column(db.Float, default=0.0, comment='工作时长（小时）')
    status = db.Column(db.String(20), default='normal', comment='状态：normal-正常, late-迟到, early_leave-早退, absent-缺勤')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<AttendanceRecord {self.user_id} {self.attendance_date}>'
    
    def calculate_work_hours(self):
        """计算工作时长"""
        if self.check_in_time and self.check_out_time:
            delta = self.check_out_time - self.check_in_time
            self.work_hours = round(delta.total_seconds() / 3600, 2)
        return self.work_hours
    
    def check_status(self, work_start_time='09:00', work_end_time='18:00'):
        """检查打卡状态"""
        if not self.check_in_time:
            self.status = 'absent'
            return
        
        # 解析工作时间
        start_hour, start_minute = map(int, work_start_time.split(':'))
        end_hour, end_minute = map(int, work_end_time.split(':'))
        work_start = time(start_hour, start_minute)
        work_end = time(end_hour, end_minute)
        
        # 检查上班时间
        check_in_time_only = self.check_in_time.time()
        if check_in_time_only > work_start:
            # 迟到判断（超过30分钟算迟到）
            start_delta = datetime.combine(date.today(), check_in_time_only) - datetime.combine(date.today(), work_start)
            if start_delta.total_seconds() > 30 * 60:
                self.status = 'late'
            else:
                self.status = 'normal'
        else:
            self.status = 'normal'
        
        # 检查下班时间
        if self.check_out_time:
            check_out_time_only = self.check_out_time.time()
            if check_out_time_only < work_end:
                # 早退
                if self.status == 'normal':
                    self.status = 'early_leave'
                elif self.status == 'late':
                    self.status = 'late_early_leave'
            self.calculate_work_hours()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else '',
            'attendance_date': self.attendance_date.strftime('%Y-%m-%d') if self.attendance_date else None,
            'check_in_time': self.check_in_time.strftime('%Y-%m-%d %H:%M:%S') if self.check_in_time else None,
            'check_out_time': self.check_out_time.strftime('%Y-%m-%d %H:%M:%S') if self.check_out_time else None,
            'work_hours': self.work_hours,
            'status': self.status,
            'status_text': self.get_status_text(),
            'remark': self.remark,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def get_status_text(self):
        """获取状态文本"""
        status_map = {
            'normal': '正常',
            'late': '迟到',
            'early_leave': '早退',
            'late_early_leave': '迟到且早退',
            'absent': '缺勤'
        }
        return status_map.get(self.status, '未知')

