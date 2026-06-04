import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base


class ApplicationStatus(str, enum.Enum):
    SAVED = "saved"
    APPLIED = "applied"
    PHONE_SCREEN = "phone_screen"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        Index("ix_applications_user_id_status", "user_id", "status"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=True)
    job_url = Column(String(2048), nullable=True)
    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.SAVED,
        nullable=False,
    )
    notes = Column(Text, nullable=True)
    applied_at = Column(Date, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", back_populates="applications")
    generated_resumes = relationship(
        "GeneratedResume", back_populates="application", cascade="all, delete-orphan"
    )
    interview_preps = relationship(
        "InterviewPrep", back_populates="application", cascade="all, delete-orphan"
    )
